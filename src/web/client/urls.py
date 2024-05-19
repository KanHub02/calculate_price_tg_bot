from django.urls import path

from .api.views import CreateLogisticRequest, CreateTelegramClient

urlpatterns = [
    path(
        "api/v1/create-logistic-request/",
        CreateLogisticRequest.as_view(),
        name="create-logistic-request",
    ),
    path(
        "api/v1/create-telegram-user/",
        CreateTelegramClient.as_view(),
        name="create-telegram-user",
    )
]
