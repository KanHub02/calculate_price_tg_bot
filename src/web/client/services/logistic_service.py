from typing import Union

import logging
from logistic.models import (
    CargoType,
    CargoPackage,
    CargoServiceType,
    CargoInsurancePrice,
    CargoTypeRange,
)
from ..models import LogisticRequest, TelegramClient, CargoServicePrice
from ..utils import calculate_price

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("LOGISTIC_SERVICE")

class LogisticRequestService:
    _model = LogisticRequest

    @classmethod
    def create_request(cls, validated_data):
        logger.info("Начало create_request с validated_data: %s", validated_data)

        cargo_type = CargoType.objects.get(id=validated_data["cargo_type_id"])
        logger.info("Тип груза получен: %s", cargo_type.title)

        cargo_package = CargoPackage.objects.get(id=validated_data["cargo_package_type_id"])
        logger.info("Тип упаковки груза получен: %s", cargo_package.title)

        telegram_client = TelegramClient.objects.get(tg_id=validated_data["tg_client_id"])
        logger.info("Клиент Telegram получен: %s", telegram_client.tg_username)

        logistic_request = cls._model(
            telegram_client=telegram_client,
            cargo_type=cargo_type,
            cargo_package_type=cargo_package,
            weight=validated_data["weight"],
            volume=validated_data["volume"],
            price_before_insurance=validated_data["price_before_insurance"],
        )
        logistic_request.save()
        logger.info("Запрос на логистику создан и сохранен: %s", logistic_request.id)

        # Calculate density
        density = logistic_request.weight / logistic_request.volume
        logistic_request.density = density
        logistic_request.save()
        logger.info("Плотность вычислена и сохранена: %f", density)

        # Calculate insurance cost
        price_per_weight = logistic_request.price_before_insurance / logistic_request.weight
        logger.info("Цена на единицу веса вычислена: %f", price_per_weight)

        insurance_cost_range = CargoInsurancePrice.objects.filter(
            min_quantity__lte=price_per_weight,
            max_quantity__gte=price_per_weight,
        ).first()

        if insurance_cost_range:
            insurance_percentage = insurance_cost_range.price
            insurance_cost = (logistic_request.price_before_insurance * insurance_percentage) / 100
            logger.info("Цена страховки вычислена: %f", insurance_cost)
        else:
            insurance_cost = 0
            logger.info("Диапазон цены страховки не найден, цена страховки установлена в 0")

        logistic_request.insurance_cost = insurance_cost
        logistic_request.save()

        # Calculate packaging cost
        package_price_per_volume = float(cargo_package.price_per_cube)
        logger.info("Цена упаковки на объем получена: %f", package_price_per_volume)

        packaging_cost = package_price_per_volume * logistic_request.volume
        logger.info("Цена упаковки вычислена: %f", packaging_cost)

        express_service_costs = []
        standard_service_costs = []

        # Calculate service costs
        service_types = CargoServiceType.objects.filter(cargo_type=cargo_type)
        total_express = 0
        total_standard = 0
        detail_express: str = f"0/кг"
        detail_standard: str = f"0/кг"
        for service_type in service_types:
            logger.info(f"SERVICE_TYPE: {service_type.name}")
            price_per_kg: Union[str, float] = calculate_price(service_type.name, cargo_type.title, logistic_request.density)
            if isinstance(price_per_kg, float):
                service_cost = price_per_kg
                CargoServicePrice.objects.create(
                    logistic_request=logistic_request,
                    cargo_service=service_type,
                    price=service_cost,
                )

                if "Express" in service_type.name:
                    detail_express = f"{service_cost}$/кг"
                    total_express = (service_cost * logistic_request.weight) + packaging_cost + insurance_cost
                    logger.info("Цена услуги Express вычислена и сохранена: %s - %f", service_type.name, service_cost)
                elif "Standart" in service_type.name:
                    detail_standard = f"{service_cost}$/кг"
                    total_standard = (service_cost * logistic_request.weight) + packaging_cost + insurance_cost
                    logger.info("Цена услуги Standard вычислена и сохранена: %s - %f", service_type.name, service_cost)

        # Calculate total costs
        # Формирование ответа в требуемом формате
        response_data = {
            "Вид товара": cargo_type.title,
            "Вес": round(logistic_request.weight, 2),
            "Куб": round(logistic_request.volume, 2),
            "Упаковка": round(packaging_cost, 2),
            "Страховка": round(insurance_cost, 2),
            "Express": detail_express,
            "Standart": detail_standard,
            "Итого Express": round(total_express, 2) if isinstance(total_express, float) else  0,
            "Итого Standart": round(total_standard, 2) if isinstance(total_standard, float) else 0,
        }

        logger.info("Данные ответа подготовлены: %s", response_data)

        return response_data
