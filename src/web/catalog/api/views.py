from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import CatalogCategory, CatalogProduct
from .serializers import CatalogCategorySerializer, CatalogCategoryDetailSerializer, CatalogProductSerializer

class MainCategoryListView(generics.ListAPIView):
    queryset = CatalogCategory.objects.filter(parent__isnull=True)
    serializer_class = CatalogCategorySerializer

class SubcategoryListView(generics.ListAPIView):
    serializer_class = CatalogCategorySerializer

    def get_queryset(self):
        parent_id = self.kwargs['pk']
        return CatalogCategory.objects.filter(parent_id=parent_id)

class SubcategoryProductsView(generics.ListAPIView):
    serializer_class = CatalogProductSerializer

    def get_queryset(self):
        category_id = self.kwargs['pk']
        category = CatalogCategory.objects.get(pk=category_id)
        subcategories = category.get_descendants(include_self=True)
        return CatalogProduct.objects.filter(category__in=subcategories)
