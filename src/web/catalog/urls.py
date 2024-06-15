from django.urls import path

from .api.views import CategoryRetrievApiView, CategoryListApiView


urlpatterns = [
    path(
        "api/v1/get-category-list/",
        CategoryListApiView.as_view(),
        name="get-category-list",
    ),
    path(
        "api/v1/get-category-retrieve/<str:pk>/",
        CategoryRetrievApiView.as_view(),
        name="get-category-retrieve",
    ),
]
