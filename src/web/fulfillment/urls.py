from django.urls import path

from .api.views import (
    MarkingPriceView,
    DoubleMarkingPriceView,
    StandardPackingPriceView,
    AssemblyPriceView,
    TaggingPriceView,
    InsertsPriceView,
    StackingPriceView,
)


urlpatterns = [
    path(
        "api/v1/get-marking-price/",
        MarkingPriceView.as_view(),
        name="get-marking-price",
    ),
    path(
        "api/v1/get-double-price/",
        DoubleMarkingPriceView.as_view(),
        name="get-double-price",
    ),
    path(
        "api/v1/get-standart-packing-price/",
        StandardPackingPriceView.as_view(),
        name="get-standart-packing-price",
    ),
    path(
        "api/v1/get-assembly-price/",
        AssemblyPriceView.as_view(),
        name="get-assembly-price",
    ),
    path(
        "api/v1/get-tagging-price/",
        TaggingPriceView.as_view(),
        name="get-tagging-price",
    ),
    path(
        "api/v1/get-insert-price/", InsertsPriceView.as_view(), name="get-insert-price"
    ),
    path(
        "api/v1/get-stacking-price/",
        StackingPriceView.as_view(),
        name="get-stacking-price",
    ),
]
