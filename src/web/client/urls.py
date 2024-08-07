from django.urls import path

from .api.views import (
    CreateLogisticRequest,
    CreateTelegramClient,
    CreateFulfillmentRequest,
    GetInfoFulfillment,
    GetInfoLogisticRequest,
    CreateFeedbackForUseful,
)

urlpatterns = [
    path(
        "api/v1/create-feedback-usefull/",
        CreateFeedbackForUseful.as_view(),
        name="create-logistic-request",
    ),
    path(
        "api/v1/create-logistic-request/",
        CreateLogisticRequest.as_view(),
        name="create-logistic-request",
    ),
    path(
        "api/v1/create-telegram-user/",
        CreateTelegramClient.as_view(),
        name="create-telegram-user",
    ),
    path(
        "api/v1/create-fulfillment-request/",
        CreateFulfillmentRequest.as_view(),
        name="create-fulfillment-request",
    ),
    path(
        "api/v1/get-fulfillment-check/<str:pk>",
        GetInfoFulfillment.as_view(),
        name="get-fulfillment-check",
    ),
    path(
        "api/v1/get-logistic-check/<str:pk>",
        GetInfoLogisticRequest.as_view(),
        name="get-logistic-check",
    ),
]
