from django.urls import path
from .api.views import (
    GetCargoList,
    GetCargoPackageList,
    GetMarkingTypeList,
    GetFulfillmentPackageList,
    FulfillmentRetieveApiView,
    CheckForDefectsView
)

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
    path(
        "api/v1/get-ff-packages/",
        GetFulfillmentPackageList.as_view(),
        name="get-ff-packages",
    ),
    path(
        "api/v1/get-ff-marks/",
        GetMarkingTypeList.as_view(),
        name="get-ff-marks",
    ),
    path(
        "api/v1/get-ff-package-sizes/<str:pk>/",
        FulfillmentRetieveApiView.as_view(),
        name="get-ff-packages",
    ),
    path(
        "api/v1/get-ff-checkdefects-types/", CheckForDefectsView.as_view(),
        name="get-ff-packages"
    )
]
