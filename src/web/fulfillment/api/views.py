from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import (
    MarkingPrice,
    DoubleMarkingPrice,
    StandardPackingPrice,
    AssemblyPrice,
    TaggingPrice,
    InsertsPrice,
    StackingPrice,
)
from .serializers import (
    MarkingPriceSerializer,
    DoubleMarkingPriceSerializer,
    StandardPackingPriceSerializer,
    AssemblyPriceSerializer,
    TaggingPriceSerializer,
    InsertsPriceSerializer,
    StackingPriceSerializer,
)


class SingletonView(APIView):
    model = None
    serializer_class = None

    def get(self, request):
        instance = self.model.load()
        serializer = self.serializer_class(instance)
        return Response(serializer.data)


class MarkingPriceView(SingletonView):
    model = MarkingPrice
    serializer_class = MarkingPriceSerializer


class DoubleMarkingPriceView(SingletonView):
    model = DoubleMarkingPrice
    serializer_class = DoubleMarkingPriceSerializer


class StandardPackingPriceView(SingletonView):
    model = StandardPackingPrice
    serializer_class = StandardPackingPriceSerializer


class AssemblyPriceView(SingletonView):
    model = AssemblyPrice
    serializer_class = AssemblyPriceSerializer


class TaggingPriceView(SingletonView):
    model = TaggingPrice
    serializer_class = TaggingPriceSerializer


class InsertsPriceView(SingletonView):
    model = InsertsPrice
    serializer_class = InsertsPriceSerializer


class StackingPriceView(SingletonView):
    model = StackingPrice
    serializer_class = StackingPriceSerializer
