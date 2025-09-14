from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet

from app_run.models import Position
from app_run.serializers import PositionSerializer

__all__ = [
    'PositionViewSet',
]


class PositionViewSet(ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('run',)
