from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import ManagerListSerializer, GetManagerChatIDSerializer, ReviewFormLinkSerializer
from ..models import Manager, ReviewFormLink


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
    
