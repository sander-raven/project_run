from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
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


class RunPagination(PageNumberPagination):
    page_size_query_param = 'size'


class RunViewSet(ModelViewSet):
    queryset = Run.objects.all().select_related('athlete')
    serializer_class = RunSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ('athlete', 'status')
    ordering_fields = ('created_at',)
    pagination_class = RunPagination


def change_run_status(
        run_id: int,
        current_status: Run.Status,
        new_status: Run.Status,
) -> Response:
    """Change run status"""
    run = get_object_or_404(Run, pk=run_id)
    if run.status == current_status:
        run.status = new_status
        run.save()
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


class StartRunView(APIView):
    def post(self, request, run_id: int):
        return change_run_status(
            run_id=run_id,
            current_status=Run.Status.INIT,
            new_status=Run.Status.IN_PROGRESS,
        )


class StopRunView(APIView):
    def post(self, request, run_id: int):
        return change_run_status(
            run_id=run_id,
            current_status=Run.Status.IN_PROGRESS,
            new_status=Run.Status.FINISHED,
        )


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
