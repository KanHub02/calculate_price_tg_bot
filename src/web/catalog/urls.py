from django.urls import path
from .api.views import (
    MainCategoryListView,
    SubcategoryListView,
    SubcategoryProductsView,
)

urlpatterns = [
    path("categories/", MainCategoryListView.as_view(), name="main-category-list"),
    path(
        "categories/<str:pk>/subcategories/",
        SubcategoryListView.as_view(),
        name="subcategory-list",
    ),
    path(
        "categories/<str:pk>/products/",
        SubcategoryProductsView.as_view(),
        name="subcategory-products",
    ),
]
