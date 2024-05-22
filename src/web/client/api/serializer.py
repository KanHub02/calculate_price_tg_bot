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


class CreateFullfillmentSerializer(serializers.Serializer):
    tg_client_id = serializers.UUIDField(required=True)
    marking_type_id = serializers.UUIDField(required=True)
    package_id = serializers.UUIDField(required=True)
    packaging_size = serializers.CharField(required=True)
    stock_id = serializers.UUIDField(required=True)
    product_title = serializers.CharField(required=True)
    quantity = serializers.FloatField(required=True)
    need_attachment = serializers.BooleanField(required=True)
    need_taging = serializers.BooleanField(required=True)
    count_of_boxes = serializers.FloatField(required=True)
    honest_sign = serializers.CharField(required=False)
