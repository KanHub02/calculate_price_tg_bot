from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from .serializer import (
    ArticleDetailSerializer,
    ArticleListSerializer,
    RestOtherSerializer,
    ScammersSerializer
)

from ..models import Article, RestOther, Scammers


class ArticleListApiView(APIView):

    serializer_class = ArticleListSerializer

    def get_queryset(self):
        qs = Article.objects.filter(is_deleted=False)
        return qs

    def get(self, request):
        qs = self.get_queryset()
        serializer = self.serializer_class(instance=qs, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class ArticleDetailApiView(APIView):

    serializer_class = ArticleDetailSerializer

    def get_instance(self, pk):
        instance = Article.objects.filter(id=pk).first()
        return instance

    def get(self, request, pk):
        instance = self.get_instance(pk=pk)
        if instance:
            serializer = self.serializer_class(instance=instance, many=False)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data=[])


class RestOtherListApiView(APIView):
    serializer_class = RestOtherSerializer

    def get_queryset(self):
        qs = RestOther.objects.filter(is_deleted=False)
        return qs

    def get(self, request):
        qs = self.get_queryset()
        serializer = self.serializer_class(instance=qs, many=True)
        return Response(data=serializer.data, status=200)


class ScammersArticleApiView(APIView):
    def get(self, request):
        qs = Scammers.objects.first()
        serializer = ScammersSerializer(qs, many=False)
        return Response(data=serializer.data, status=status.HTTP_200_OK)