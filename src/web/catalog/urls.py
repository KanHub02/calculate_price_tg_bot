from django.urls import path
from .api.views import CategoryRetrieveApiView, CategoryListApiView

urlpatterns = [
    path(
        "api/v1/get-category-list/",
        CategoryListApiView.as_view(),
        name="get-category-list",
    ),
    path(
        "api/v1/get-category-retrieve/<str:pk>/",
        CategoryRetrieveApiView.as_view(),
        name="get-category-retrieve",
    ),
]
