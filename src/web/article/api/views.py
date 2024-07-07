from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from .serializer import ArticleDetailSerializer, ArticleListSerializer

from ..models import Article


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
    