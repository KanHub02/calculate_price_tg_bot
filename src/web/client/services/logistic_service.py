from fulfillment.models import CargoType, CargoPackage, CargoServiceType, CargoInsurancePrice

from ..models import LogisticRequest, TelegramClient, CargoServicePrice
from ..utils import calculate_price


class LogisticRequestService:
    _model = LogisticRequest

    @classmethod
    def create_request(cls, validated_data):
        cargo_type = CargoType.objects.get(id=validated_data["cargo_type_id"])
        cargo_package = CargoPackage.objects.get(id=validated_data["cargo_package_type_id"])
        telegram_client = TelegramClient.objects.get(tg_id=validated_data["tg_client_id"])

        logistic_request = cls._model(
            telegram_client=telegram_client,
            cargo_type=cargo_type,
            cargo_package_type=cargo_package,
            weight=validated_data["weight"],
            volume=validated_data["volume"],
            price_before_insurance=validated_data["price_before_insurance"]
        )
        logistic_request.save()

        price_per_weight = logistic_request.price_before_insurance / logistic_request.weight
        insurance_cost_range = CargoInsurancePrice.objects.filter(
            min_quantity__lte=price_per_weight,
            max_quantity__gte=price_per_weight,
        ).first()
        if insurance_cost_range:
            insurance_percentage = insurance_cost_range.price
            print("Процентаж", insurance_percentage)
            insurance_cost = (logistic_request.price_before_insurance * insurance_percentage) / 100
        else:
            insurance_cost = 0  # Если нет подходящего диапазона
        
        logistic_request.insurance_cost = insurance_cost
        logistic_request.save()
        print("Цена", logistic_request.price_before_insurance)
        print("Цена страховки", insurance_cost)
        cube = logistic_request.volume / logistic_request.weight
        logistic_request.cube = cube
        logistic_request.save()

        package_price_per_cube = float(cargo_package.price_per_cube)  # Убедитесь, что это число
        packaging_cost = package_price_per_cube * cube
        service_costs = []
        services_pricing = []
        total_express = total_standard = packaging_cost + insurance_cost

        service_types = CargoServiceType.objects.filter(cargo_type=cargo_type)
        for service_type in service_types:
            price = calculate_price(service_type.name, cargo_type.title, logistic_request.weight / cube)
            CargoServicePrice.objects.create(
                logistic_request=logistic_request,
                cargo_service=service_type,
                price=price,
            )
            services_pricing.append({"service_name": service_type.name, "price": price})
            service_costs.append(price)
            if 'Express' in service_type.name and isinstance(price, float):
                total_express += price
            if 'Standard' in service_type.name and isinstance(price, float):
                total_standard += price

        response_data = {
            "cargo_type": cargo_type.title,
            "weight": logistic_request.weight,
            "cube": logistic_request.cube,
            "packaging_type": cargo_package.title,
            "packaging_cost": packaging_cost,
            "insurance_cost": insurance_cost,
            "services_pricing": services_pricing,
            "total_express": total_express,
            "total_standard": total_standard
        }

        return response_data

