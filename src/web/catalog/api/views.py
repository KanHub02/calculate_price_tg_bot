from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from .serializers import CategorySerializer
from ..models import CatalogCategory


class CategoryListApiView(APIView):

    def get_queryset(self):
        queryset = CatalogCategory.objects.filter(is_deleted=False)
        return queryset

    def get(self, request):
        queryset = self.get_queryset()
        serializer = CategorySerializer(instance=queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class Category