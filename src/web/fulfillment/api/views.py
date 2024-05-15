from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import (
    FulfillmentType,
    CargoType
)
from .serializers import (
    FulfillmentTypeSerializer,
    CargoTypeSerializer,
)


class GetFulfillmentList(APIView):

    def get_queryset(self):
        queryset = FulfillmentType.objects.filter(is_deleted=False)
        return queryset
    
    
    def get(self, request):
        qs = self.get_queryset()
        serializer = FulfillmentTypeSerializer(instance=qs, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class GetCargoList(APIView):

    def get_queryset(self):
        queryset = CargoType.objects.filter(is_deleted=False)
        return queryset
    
    
    def get(self, request):
        qs = self.get_queryset()
        serializer = CargoTypeSerializer(instance=qs, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
