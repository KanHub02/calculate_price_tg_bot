from django.urls import path

from .api.views import GetManagerIDsApiView, ReviewFormLinkApiView, ManagerListApiView, PartnerLeadApiView, HowToUseApiView


urlpatterns = [
    path("api/v1/get-manager-card-list/", ManagerListApiView.as_view()),
    path("api/v1/get-manager-ids/", GetManagerIDsApiView.as_view()),
    path("api/v1/get-review-form/", ReviewFormLinkApiView.as_view()),
    path("api/v1/get-howtouser-info/", HowToUseApiView.as_view()),
    path("api/v1/get-partnerlead-info/", PartnerLeadApiView.as_view()),
]
