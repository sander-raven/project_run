from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from app_run.models import Run
from app_run.serializers import RunSerializer

__all__ = [
    'RunViewSet',
    'StartRunView',
    'StopRunView',
]


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
