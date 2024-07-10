from django.db.models import QuerySet

from rest_framework import serializers
from ..models import (
    FulfillmentPackage,
    MarkingType,
    FulfillmentPackage,
    FulfillmentPackageSize,
    CheckForDefectsRange,
    CheckForDefectsType,
)


class CheckForDefectsTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckForDefectsType
        fields = ("id", "title")


class MarkingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarkingType
        fields = ("id", "title")


class PackagingSizeSerializer(serializers.ModelSerializer):
    sizes = serializers.SerializerMethodField()

    class Meta:
        model = FulfillmentPackage
        fields = ["sizes"]

    def get_sizes(self, instance):
        return list(instance.fulfillment_package_size.values("size"))

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["sizes"] = self.get_sizes(instance)
        return data


class PackagingSerializer(serializers.ModelSerializer):
    class Meta:
        model = FulfillmentPackage
        fields = [
            "id",
            "title",
        ]
