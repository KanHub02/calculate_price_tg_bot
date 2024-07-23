from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import ManagerListSerializer, GetManagerChatIDSerializer, ReviewFormLinkSerializer, HowToUseSerializer, PartnerLeadSerializer, WorkingConditionsSerializer
from ..models import Manager, ReviewFormLink, HowToUse, PartnerLead, WorkingConditions


class ManagerListApiView(APIView):

    serializer_class = ManagerListSerializer

    def get_queryset(self):
        qs = Manager.objects.filter(is_deleted=False)
        return qs

    def get(self, request):
        qs = self.get_queryset()
        serializer = self.serializer_class(instance=qs, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class GetManagerIDsApiView(APIView):

    def get(self, request):
        qs = Manager.objects.filter(is_deleted=False)
        serializer = GetManagerChatIDSerializer(qs, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
class ReviewFormLinkApiView(APIView):

    def get(self, request):
        qs = ReviewFormLink.objects.filter(is_deleted=False)
        serializer = ReviewFormLinkSerializer(qs, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class HowToUseApiView(APIView):

    def get(self, request):
        qs = HowToUse.objects.first()
        serializer = HowToUseSerializer(qs, many=False)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class PartnerLeadApiView(APIView):
    def get(self, request):
        qs = PartnerLead.objects.first()
        serializer = PartnerLeadSerializer(qs, many=False)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    

class WorkingConditionsApiView(APIView):
    def get(self, request):
        qs = WorkingConditions.objects.first()
        serializer = WorkingConditionsSerializer(qs, many=False)
        return Response(data=serializer.data, status=status.HTTP_200_OK)