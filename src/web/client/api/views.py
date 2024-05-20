from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializer import TelegramClientSerializer, CreateLogisticRequestSerializer
from ..models import TelegramClient
from ..services.create_tg_client import TelegramClientService
from ..services.logistic_service import LogisticRequestService


class CreateTelegramClient(APIView):
    service = TelegramClientService

    def post(self, request):
        serializer = TelegramClientSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validated_data
            self.service.get_or_create(validated_data)
            return Response(data={"ok"}, status=status.HTTP_200_OK)


class CreateLogisticRequest(APIView):
    service = LogisticRequestService
    serializer_class = CreateLogisticRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validated_data
            self.service.create_request(validated_data=validated_data)
            return Response(data="OK", status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CalculatePriceView(APIView):
    # calculate price by id
    pass
