from django.urls import path

from .api.views import ArticleListApiView, ArticleDetailApiView, RestOtherListApiView


urlpatterns = [
    path("api/v1/article-list/", ArticleListApiView.as_view(), name="article-list"),
    path(
        "api/v1/article-detail/<str:pk>/",
        ArticleDetailApiView.as_view(),
        name="article-detail",
    ),
    path(
        "api/v1/other-list/", RestOtherListApiView.as_view(), name="api/v1/other-list/"
    ),
]
