from rest_framework import serializers

from ..models import TelegramClient, LogisticRequest


class TelegramClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramClient
        fields = ("tg_username", "tg_id", "phone_number", "tg_bio")


class CreateLogisticRequestSerializer(serializers.Serializer):
    tg_client_id = serializers.CharField(required=True)
    cargo_type_id = serializers.UUIDField(required=True)
    cargo_package_type_id = serializers.UUIDField(required=True)
    weight = serializers.FloatField(required=True)
    quantity = serializers.FloatField(required=True)
    volume = serializers.FloatField(required=True)
    insurance_cost = serializers.FloatField(required=True)
