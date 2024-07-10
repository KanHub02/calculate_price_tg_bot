from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializer import (
    TelegramClientSerializer,
    CreateLogisticRequestSerializer,
    CreateFullfillmentSerializer,
    FulfillmentRequestDetail,
    LogisticRequestSerializer,
    CreateFeedbackForUsefulSerializer,
)
from ..models import (
    TelegramClient,
    FulFillmentRequest,
    LogisticRequest,
    FeedbackForUseful,
)
from ..services.create_tg_client import TelegramClientService
from ..services.logistic_service import LogisticRequestService
from ..services.fulfillments_service import FulfillmentService


class CreateFeedbackForUseful(APIView):
    serializer_class = CreateFeedbackForUsefulSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validated_data
            tg_user = TelegramClient.objects.filter(
                tg_id=validated_data.get("telegram_client_id")
            ).first()
            if tg_user:
                FeedbackForUseful.objects.create(
                    telegram_client=tg_user, feedback=validated_data.get("feedback")
                )
                return Response(data="ok", status=status.HTTP_200_OK)

        return Response(data=serializer.errors, status=status.HTTP_200_OK)


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
            response_data = self.service.create_request(validated_data=validated_data)
            return Response(data=response_data, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateFulfillmentRequest(APIView):
    service = FulfillmentService
    serializer_class = CreateFullfillmentSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validated_data
            ff_id = self.service.create_request(validated_data=validated_data)
            return Response(data={"ff_id": ff_id}, status=status.HTTP_200_OK)

        else:
            return Response(data=serializer.errors)


class GetInfoFulfillment(APIView):
    serializer_class = FulfillmentRequestDetail

    def get(self, request, pk):
        instance = FulFillmentRequest.objects.filter(id=pk).first()
        if instance:
            data = self.serializer_class(instance=instance).data
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            return Response(data="Not Found", status=status.HTTP_404_NOT_FOUND)


class GetInfoLogisticRequest(APIView):
    serializer_class = LogisticRequestSerializer

    def get(self, request, pk):
        instance = LogisticRequest.objects.filter(id=pk).first()
        if instance:
            data = self.serializer_class(instance=instance).data
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            return Response(data="Not Found", status=status.HTTP_404_NOT_FOUND)
