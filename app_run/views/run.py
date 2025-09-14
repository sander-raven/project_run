from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from app_run.models import Challenge, Run
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


class StartRunView(APIView):
    def post(self, request, run_id: int):
        run = get_object_or_404(Run, pk=run_id)
        result = run.change_status(new_status=Run.Status.IN_PROGRESS)
        if result:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class StopRunView(APIView):
    def post(self, request, run_id: int):
        run = get_object_or_404(Run, pk=run_id)
        result = run.change_status(new_status=Run.Status.FINISHED)
        if result:
            athlete_finished_run_count = Run.objects.filter(
                athlete_id=run.athlete_id,
                status=Run.Status.FINISHED,
            ).count()
            if athlete_finished_run_count == 10:
                Challenge.objects.create(
                    full_name='Сделай 10 Забегов!',
                    athlete_id=run.athlete_id,
                )
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
