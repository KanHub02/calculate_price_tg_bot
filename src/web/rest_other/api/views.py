from rest_framework.views import APIView
from rest_framework.response import Response


from .serializers import RestOtherSerializer
from ..models import RestOther


class RestOtherListApiView(APIView):
    serializer_class = RestOtherSerializer
    
    def get_queryset(self):
        qs = RestOther.objects.filter(is_deleted=False)
        return qs
    
    def get(self, request):
        qs = self.get_queryset()
        serializer = self.serializer_class(instance=qs, many=True)
        return Response(data=serializer.data, status=200)
