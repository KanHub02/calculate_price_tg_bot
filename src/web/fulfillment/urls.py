from django.urls import path
from .api.views import (
    GetMarkingTypeList,
    GetFulfillmentPackageList,
    FulfillmentRetieveApiView,
    CheckForDefectsView
)

urlpatterns = [
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
