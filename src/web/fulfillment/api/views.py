from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from ..models import (
    MarkingType,
    MarkingType,
    FulfillmentPackage,
    CheckForDefectsType
)
from .serializers import (
    MarkingTypeSerializer,
    PackagingSerializer,
    PackagingSizeSerializer,
    CheckForDefectsTypeSerializer
)


# class GetFulfillmentList(APIView):
#     def get_queryset(self):
#         queryset = MarkingType.objects.filter(is_deleted=False)
#         return queryset
#
#     def get(self, request):
#         qs = self.get_queryset()
#         serializer = FulfillmentTypeSerializer(instance=qs, many=True)
#         return Response(data=serializer.data, status=status.HTTP_200_OK)


class GetMarkingTypeList(APIView):
    def get_queryset(self):
        queryset = MarkingType.objects.filter(is_deleted=False)
        return queryset

    def get(self, request):
        qs = self.get_queryset()
        serializer = MarkingTypeSerializer(instance=qs, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class CheckForDefectsView(APIView):
    def get_queryset(self):
        queryset = CheckForDefectsType.objects.filter(is_deleted=False)
        return queryset

    def get(self, request):
        qs = self.get_queryset()
        serializer = CheckForDefectsTypeSerializer(instance=qs, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    


class GetFulfillmentPackageList(APIView):
    def get_queryset(self):
        queryset = FulfillmentPackage.objects.filter(is_deleted=False)
        return queryset

    def get(self, request):
        qs = self.get_queryset()
        serializer = PackagingSerializer(instance=qs, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class FulfillmentRetieveApiView(RetrieveAPIView):
    def get_queryset(self, pk):
        queryset = FulfillmentPackage.objects.filter(is_deleted=False, pk=pk)
        return queryset

    def get(self, request, pk):
        qs = self.get_queryset(pk)
        serializer = PackagingSizeSerializer(instance=qs.first())
        return Response(data=serializer.data, status=status.HTTP_200_OK)
