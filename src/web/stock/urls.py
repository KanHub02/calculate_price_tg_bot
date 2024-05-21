from django.urls import path
from .api.views import GetStockListView

urlpatterns = [
    path("api/v1/get-stock-list/", GetStockListView.as_view(), name="get-stock-list"),
]
