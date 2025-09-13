from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .helpers import get_company_details, get_user_type_query
from .models import Run
from .serializers import RunSerializer, UserSerializer

User = get_user_model()


@api_view(['GET'])
def company_details(request):
    return Response(get_company_details())


class RunViewSet(ModelViewSet):
    queryset = Run.objects.all().select_related('athlete')
    serializer_class = RunSerializer


class StartRunView(APIView):
    def post(self, request, run_id: int):
        run = get_object_or_404(Run, pk=run_id)
        if run.status == Run.Status.INIT:
            run.status = Run.Status.IN_PROGRESS
            run.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('first_name', 'last_name')

    def get_queryset(self):
        qs = self.queryset
        user_type = self.request.query_params.get('type', None)
        query = get_user_type_query(user_type)
        return qs.filter(query).exclude(is_superuser=True)
