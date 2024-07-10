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
        logger.info("Starting create_request with validated_data: %s", validated_data)

        cargo_type = CargoType.objects.get(id=validated_data["cargo_type_id"])
        logger.info("Cargo type retrieved: %s", cargo_type.title)

        cargo_package = CargoPackage.objects.get(
            id=validated_data["cargo_package_type_id"]
        )
        logger.info("Cargo package type retrieved: %s", cargo_package.title)

        telegram_client = TelegramClient.objects.get(
            tg_id=validated_data["tg_client_id"]
        )
        logger.info("Telegram client retrieved: %s", telegram_client.tg_username)

        logistic_request = cls._model(
            telegram_client=telegram_client,
            cargo_type=cargo_type,
            cargo_package_type=cargo_package,
            weight=validated_data["weight"],
            volume=validated_data["volume"],
            price_before_insurance=validated_data["price_before_insurance"],
        )
        logistic_request.save()
        logger.info("Logistic request created and saved: %s", logistic_request.id)

        # Calculate density
        density = logistic_request.weight / logistic_request.volume
        logistic_request.density = density
        logistic_request.save()
        logger.info("Density calculated and saved: %f", density)

        # Calculate insurance cost
        price_per_weight = (
            logistic_request.price_before_insurance / logistic_request.weight
        )
        logger.info("Price per weight calculated: %f", price_per_weight)

        insurance_cost_range = CargoInsurancePrice.objects.filter(
            min_quantity__lte=price_per_weight,
            max_quantity__gte=price_per_weight,
        ).first()

        if insurance_cost_range:
            insurance_percentage = insurance_cost_range.price
            insurance_cost = (
                logistic_request.price_before_insurance * insurance_percentage
            ) / 100
            logger.info("Insurance cost calculated: %f", insurance_cost)
        else:
            insurance_cost = 0
            logger.info("No insurance cost range found, insurance cost set to 0")

        logistic_request.insurance_cost = insurance_cost
        logistic_request.save()

        # Calculate packaging cost
        package_price_per_volume = float(cargo_package.price_per_cube)
        logger.info("Package price per volume retrieved: %f", package_price_per_volume)

        packaging_cost = package_price_per_volume * logistic_request.volume
        logger.info("Packaging cost calculated: %f", packaging_cost)

        express_service_costs = []
        standard_service_costs = []

        # Calculate service costs
        service_types = CargoServiceType.objects.filter(cargo_type=cargo_type)
        for service_type in service_types:
            price_per_kg = calculate_price(
                service_type.name, cargo_type.title, logistic_request.density
            )
            if isinstance(price_per_kg, str):
                logger.warning("Service price calculation warning: %s", price_per_kg)
                if "Express" in service_type.name:
                    express_service_costs.append((service_type.name, price_per_kg))
                elif "Standard" in service_type.name:
                    standard_service_costs.append((service_type.name, price_per_kg))
            else:
                service_cost = logistic_request.weight * price_per_kg
                CargoServicePrice.objects.create(
                    logistic_request=logistic_request,
                    cargo_service=service_type,
                    price=service_cost,
                )
                if "Express" in service_type.name:
                    express_service_costs.append((service_type.name, service_cost))
                    logger.info(
                        "Express service cost calculated and saved: %s - %f",
                        service_type.name,
                        service_cost,
                    )
                elif "Standard" in service_type.name:
                    standard_service_costs.append((service_type.name, service_cost))
                    logger.info(
                        "Standard service cost calculated and saved: %s - %f",
                        service_type.name,
                        service_cost,
                    )

        # Calculate total costs
        total_express = (
            sum(cost for _, cost in express_service_costs if isinstance(cost, float))
            + packaging_cost
            + insurance_cost
        )
        total_standard = (
            sum(cost for _, cost in standard_service_costs if isinstance(cost, float))
            + packaging_cost
            + insurance_cost
        )

        # Формирование ответа в требуемом формате
        response_data = {
            "Вид товара": cargo_type.title,
            "Вес": logistic_request.weight,
            "Куб": logistic_request.volume,
            "Упаковка": packaging_cost,
            "Страховка": insurance_cost,
            "Express": total_express,
            "Standart": total_standard,
            "Express details": express_service_costs,
            "Standart details": standard_service_costs,
        }

        logger.info("Response data prepared: %s", response_data)

        return response_data
