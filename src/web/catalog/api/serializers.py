from rest_framework import serializers
from ..models import CatalogCategory, CatalogProduct, Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogCategory
        fields = ("id", "title")

class ProductSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = CatalogProduct
        fields = ["title", "file", "tags"]

class CategoryProductSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    class Meta:
        model = CatalogCategory
        fields = ["products"]

    def get_products(self, instance: CatalogCategory):
        request = self.context.get('request')
        tags = request.query_params.getlist('tags')
        products = instance.get_descendants(include_self=True).values_list('product', flat=True)
        products = CatalogProduct.objects.filter(pk__in=products)

        if tags:
            products = products.filter(tags__name__in=tags).distinct()

        return ProductSerializer(products, many=True).data

    def to_representation(self, instance: CatalogCategory):
        data = super().to_representation(instance)
        data["products"] = self.get_products(instance)
        return data
