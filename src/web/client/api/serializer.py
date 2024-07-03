from rest_framework import serializers

from ..models import (
    TelegramClient,
    LogisticRequest,
    FulFillmentRequest,
    CargoServicePrice,
)


class TelegramClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramClient
        fields = ("tg_username", "tg_id", "phone_number", "tg_bio")


class CreateLogisticRequestSerializer(serializers.Serializer):
    tg_client_id = serializers.CharField(required=True)
    cargo_type_id = serializers.UUIDField(required=True)
    cargo_package_type_id = serializers.UUIDField(required=True)
    weight = serializers.FloatField(required=True)
    volume = serializers.FloatField(required=True)
    price_before_insurance = serializers.FloatField(required=True)


class CreateFullfillmentSerializer(serializers.Serializer):
    tg_client_id = serializers.CharField(required=True)
    marking_type_id = serializers.UUIDField(required=True)
    defect_check_id = serializers.UUIDField(required=False)
    package_id = serializers.UUIDField(required=True)
    packaging_size = serializers.CharField(required=True)
    stock_id = serializers.UUIDField(required=True)
    product_title = serializers.CharField(required=True)
    quantity = serializers.FloatField(required=True)
    need_attachment = serializers.BooleanField(required=True)
    need_taging = serializers.BooleanField(required=True)
    count_of_boxes = serializers.FloatField(required=True)
    honest_sign = serializers.BooleanField(required=False)


class FulfillmentRequestDetail(serializers.ModelSerializer):
    marking_type_title = serializers.CharField(
        source="marking_type.title", read_only=True
    )
    package_title = serializers.CharField(source="package.title", read_only=True)
    check_defects_title = serializers.CharField(source="need_check_defects.title", read_only=True)

    class Meta:
        model = FulFillmentRequest
        fields = (
            "product_title",
            "quantity",
            "marking_type_title",
            "check_defects_title",
            "honest_sign",
            "package_title",
            "packaging_size",
            "need_taging",
            "need_attachment",
            "count_of_boxes",
            "per_price_ff",
            "per_price_transit",
            "per_price_material",
        )


class CargoServicePriceSerializer(serializers.ModelSerializer):
    service_type = serializers.CharField(source="cargo_service.service_type")

    class Meta:
        model = CargoServicePrice
        fields = ["price", "service_type"]


class LogisticRequestSerializer(serializers.ModelSerializer):
    express_price = serializers.SerializerMethodField()
    standard_price = serializers.SerializerMethodField()
    total_express = serializers.SerializerMethodField()
    total_standard = serializers.SerializerMethodField()
    cargo_type = serializers.CharField(
        source="cargo_type.title"
    )  # Assuming there is a descriptive field
    cargo_package_type = serializers.CharField(source="cargo_package_type.title")

    class Meta:
        model = LogisticRequest
        fields = [
            "cargo_type",
            "weight",
            "quantity",
            "cargo_package_type",
            "insurance_cost",
            "express_price",
            "standard_price",
            "total_express",
            "total_standard",
        ]

    def get_express_price(self, obj):
        return self.get_service_price(obj, "Express")

    def get_standard_price(self, obj):
        return self.get_service_price(obj, "Standard")

    def get_service_price(self, obj, service_name):
        # Correctly filter related CargoServicePrice by service type through CargoServiceType
        service_price = CargoServicePrice.objects.filter(
            logistic_request=obj,
            cargo_service__service_type__service_name=service_name,  # Adjust based on actual field names
        ).first()
        return service_price.price if service_price else 0

    def get_total_express(self, obj):
        # Calculate the total cost for Express service
        return obj.quantity * self.get_express_price(obj)

    def get_total_standard(self, obj):
        # Calculate the total cost for Standard service
        return obj.quantity * self.get_standard_price(obj)
