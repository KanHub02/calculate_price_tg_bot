from django.urls import path

from .api.views import ArticleListApiView, ArticleDetailApiView


urlpatterns = [
    path("api/v1/article-list/", ArticleListApiView.as_view(), name="article-list"),
    path("api/v1/article-detail/<str:pk>/", ArticleDetailApiView.as_view(), name="article-detail"),
]
