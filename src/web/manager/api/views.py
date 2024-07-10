from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import ManagerListSerializer
from ..models import Manager


class ManagerListApiView(APIView):

    serializer_class = ManagerListSerializer

    def get_queryset(self):
        qs = Manager.objects.filter(is_deleted=False)
        return qs

    def get(self, request):
        qs = self.get_queryset()
        serializer = self.serializer_class(instance=qs, many=True)
        return Response(data=serializer.data, status=200)
