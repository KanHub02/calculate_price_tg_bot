from django.urls import path

from .api.views import GetAfterApiView, GetBeforeApiView, TranslateCryptiInfoApiView, TranslateRfInfoApiView


urlpatterns = [
    path("api/v1/get-before-course/", GetBeforeApiView.as_view()),
    path("api/v1/get-after-course/", GetAfterApiView.as_view()),
    path("api/v1/get-crypto-info/", TranslateCryptiInfoApiView.as_view()),
    path("api/v1/get-rf-info/", TranslateRfInfoApiView.as_view()),
]
