from fulfillment.models import CargoType, CargoPackage

from ..models import LogisticRequest, TelegramClient


class LogisticRequestService(object):
    _model = LogisticRequest

    @classmethod
    def create_request(cls, validated_data: dict):
        cargo_type = CargoType.objects.filter(
            id=validated_data["cargo_type_id"]
        ).first()
        cargo_package = CargoPackage.objects.filter(
            id=validated_data["cargo_package_type_id"]
        ).first()
        telegram_client = TelegramClient.objects.filter(
            tg_id=validated_data["tg_client_id"]
        ).first()
        logistic_request_instance = cls._model(
                telegram_client=telegram_client,
                cargo_type=cargo_type,
                cargo_package_type=cargo_package,
                quantity=validated_data["quantity"],
                weight=validated_data["weight"],
            )
        logistic_request_instance.save()
            # calculate prices
