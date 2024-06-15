from rest_framework import serializers

from ..models import CatalogCategory


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = CatalogCategory
        fields = (
            "id",
            "title",
        )


class CategoryProductSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    class Meta:
        model = CatalogCategory
        fields = [
            "products",
        ]

    def get_products(self, instance: CatalogCategory):
        result = list(instance.product.values("title", "file"))
        return result

    def to_representation(self, instance: CatalogCategory):
        data = super().to_representation(instance)
        data["products"] = self.get_products(instance)
        return data
