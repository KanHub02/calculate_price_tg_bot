from django.urls import path

from .api.views import ArticleListApiView


urlpatterns = [
    path("api/v1/article-list/", ArticleListApiView.as_view(), name="article-list"),
]
