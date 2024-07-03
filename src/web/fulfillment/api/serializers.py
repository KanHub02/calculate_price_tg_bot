from django.db.models import QuerySet

from rest_framework import serializers
from ..models import (
    CargoType,
    CargoPackage,
    FulfillmentPackage,
    MarkingType,
    FulfillmentPackage,
    FulfillmentPackageSize,
    CheckForDefectsRange, 
    CheckForDefectsType,
    CargoServiceType
)


class CargoTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CargoType
        fields = ("id", "title")

    # def get_ranges(self, instance: CargoType):
    #     return list(instance.cargo_type_range.values("min_quantity", "max_quantity", "price"))

    # def to_representation(self, instance: CargoType):
    #     data = super().to_representation(instance)
    #     data["ranges"] = self.get_ranges(instance)
    #     return data


class CargoPackageSerializers(serializers.ModelSerializer):
    class Meta:
        model = CargoPackage
        fields = ("id", "title")

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

    def get_sizes(self, instance: CargoType):
        return list(instance.fulfillment_package_size.values("size"))

    def to_representation(self, instance: CargoType):
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
