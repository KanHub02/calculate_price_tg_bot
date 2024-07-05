from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from .serializer import ArticleSerializer

from ..models import Article


class ArticleListApiView(APIView):

    serializer_class = ArticleSerializer

    def get_queryset(self):
        qs = Article.objects.filter(is_deleted=False)
        return qs
    
    def get(self, request):
        qs = self.get_queryset()
        serializer = self.serializer_class(instance=qs, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    