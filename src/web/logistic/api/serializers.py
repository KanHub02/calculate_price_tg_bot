from django.db.models import QuerySet

from rest_framework import serializers
from ..models import CargoType, CargoPackage, CargoServiceType


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
