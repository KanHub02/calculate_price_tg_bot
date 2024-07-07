from django.urls import path

from .api.views import RestOtherListApiView

urlpatterns = [
    path("api/v1/other-list/", RestOtherListApiView.as_view(), name="api/v1/other-list/")
]
