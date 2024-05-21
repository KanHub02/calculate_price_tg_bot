from django.urls import path

from .api.views import GetCargoList, GetCargoPackageList


urlpatterns = [
    # path(
    #     "api/v1/get-fulfillment-types/",
    #     GetFulfillmentList.as_view(),
    #     name="get-fulfillment-price",
    # ),
    path(
        "api/v1/get-cargo-types/",
        GetCargoList.as_view(),
        name="get-cargo-price",
    ),
    path(
        "api/v1/get-cargo-packages/",
        GetCargoPackageList.as_view(),
        name="get-cargo-package",
    ),
]
