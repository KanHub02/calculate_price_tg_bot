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
        fields = ["sizes",]

    def get_products(self, instance: CatalogCategory):
        return list(instance.product.values("title", "file"))

    def to_representation(self, instance: CatalogCategory):
        data = super().to_representation(instance)
        data["products"] = self.get_products(instance)
        return data
