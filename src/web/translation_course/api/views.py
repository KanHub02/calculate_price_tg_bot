from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework import status


from .serializers import AfterCourseSerializer, BeforeCourceSerializer, TranslateCryptiInfoSerializer, TranslateRfInfoSerializer
from ..models import BeforeCource, AfterCourse, TranslateCryptiInfo, TranslateRfInfo


class TranslateCryptiInfoApiView(APIView):

    def get_queryset(self):
        qs = TranslateCryptiInfo.objects.first()
        return qs
        
    def get(self, request):
        qs = self.get_queryset()
        serializer = TranslateCryptiInfoSerializer(qs, many=False)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class TranslateRfInfoApiView(APIView):

    def get_queryset(self):
        qs = TranslateRfInfo.objects.first()
        return qs
        
    def get(self, request):
        qs = self.get_queryset()
        serializer = TranslateRfInfoSerializer(qs, many=False)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class GetBeforeApiView(APIView):

    def get_queryset(self):
        qs = BeforeCource.objects.first()
        return qs
        
    def get(self, request):
        qs = self.get_queryset()
        serializer = BeforeCourceSerializer(qs, many=False)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class GetAfterApiView(APIView):

    def get_queryset(self):
        qs = AfterCourse.objects.first()
        return qs

    def get(self, request):
        qs = self.get_queryset()
        serializer = AfterCourseSerializer(qs, many=False)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
