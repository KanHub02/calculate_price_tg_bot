from fulfillment.models import CargoType, CargoPackage, CargoServiceType

from ..models import LogisticRequest, TelegramClient, CargoServicePrice
from ..utils import calculate_price


class LogisticRequestService:
    _model = LogisticRequest

    @classmethod
    def create_request(cls, validated_data):
        cargo_type = CargoType.objects.get(id=validated_data["cargo_type_id"])
        cargo_package = CargoPackage.objects.get(
            id=validated_data["cargo_package_type_id"]
        )
        telegram_client = TelegramClient.objects.get(
            tg_id=validated_data["tg_client_id"]
        )

        logistic_request = cls._model(
            telegram_client=telegram_client,
            cargo_type=cargo_type,
            cargo_package_type=cargo_package,
            quantity=validated_data["quantity"],
            weight=validated_data["weight"],
            insurance_cost=validated_data["insurance_cost"],
        )
        logistic_request.save()

        density = logistic_request.weight / logistic_request.quantity

        service_types = CargoServiceType.objects.filter(cargo_type=cargo_type)

        for service_type in service_types:
            price = calculate_price(service_type.name, cargo_type.title, density)
            if isinstance(price, float):
                CargoServicePrice.objects.create(
                    logistic_request=logistic_request,
                    cargo_service=service_type,
                    price=price,
                )

        return logistic_request
