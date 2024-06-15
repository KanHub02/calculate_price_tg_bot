from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView


from .serializers import CategorySerializer, CategoryProductSerializer
from ..models import CatalogCategory


class CategoryListApiView(APIView):

    def get_queryset(self):
        queryset = CatalogCategory.objects.filter(is_deleted=False)
        return queryset

    def get(self, request):
        queryset = self.get_queryset()
        serializer = CategorySerializer(instance=queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class CategoryRetrievApiView(RetrieveAPIView):

    def get_queryset(self, pk):
        queryset = CatalogCategory.objects.filter(is_deleted=False, pk=pk)
        return queryset

    def get(self, request, pk):
        qs = self.get_queryset(pk)
        serializer = CategoryProductSerializer(instance=qs.first())
        return Response(data=serializer.data, status=status.HTTP_200_OK)
