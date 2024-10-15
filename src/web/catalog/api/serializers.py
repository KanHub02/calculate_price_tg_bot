from rest_framework import serializers
from ..models import CatalogCategory, CatalogProduct



class CatalogProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = CatalogProduct
        fields = ["id", "title", "file"]


class CatalogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogCategory
        fields = ["id", "title", "parent"]


class CatalogCategoryDetailSerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = CatalogCategory
        fields = ["id", "title", "parent", "subcategories"]

    def get_subcategories(self, obj):
        subcategories = obj.get_children()
        return CatalogCategorySerializer(subcategories, many=True).data
