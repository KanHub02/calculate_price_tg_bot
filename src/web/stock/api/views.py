from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from .serializers import StockSerializer
from ..models import Stock


class GetStockListView(APIView):

    def get_queryset(self):
        queryset = Stock.objects.filter(is_deleted=False)
        return queryset

    def get(self, request):
        qs = self.get_queryset()
        serializer = StockSerializer(instance=qs, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
