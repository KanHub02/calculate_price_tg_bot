from rest_framework import serializers
from ..models import (
    MarkingPrice,
    DoubleMarkingPrice,
    StandardPackingPrice,
    AssemblyPrice,
    TaggingPrice,
    InsertsPrice,
    StackingPrice,
)


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["min_quantity", "max_quantity", "price"]


class MarkingPriceSerializer(PriceSerializer):
    class Meta(PriceSerializer.Meta):
        model = MarkingPrice


class DoubleMarkingPriceSerializer(PriceSerializer):
    class Meta(PriceSerializer.Meta):
        model = DoubleMarkingPrice


class StandardPackingPriceSerializer(PriceSerializer):
    class Meta(PriceSerializer.Meta):
        model = StandardPackingPrice


class AssemblyPriceSerializer(PriceSerializer):
    class Meta(PriceSerializer.Meta):
        model = AssemblyPrice


class TaggingPriceSerializer(PriceSerializer):
    class Meta(PriceSerializer.Meta):
        model = TaggingPrice


class InsertsPriceSerializer(PriceSerializer):
    class Meta(PriceSerializer.Meta):
        model = InsertsPrice


class StackingPriceSerializer(PriceSerializer):
    class Meta(PriceSerializer.Meta):
        model = StackingPrice
