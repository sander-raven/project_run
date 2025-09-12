from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .helpers import get_company_details
from .models import Run
from .serializers import RunSerializer


@api_view(['GET'])
def company_details(request):
    return Response(get_company_details())


class RunViewSet(ModelViewSet):
    queryset = Run.objects.all()
    serializer_class = RunSerializer
