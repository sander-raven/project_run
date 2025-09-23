from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet

from app_run.models import Position
from app_run.serializers import PositionSerializer
from app_run.helpers import assign_nearby_items_to_user, calculate_position_distance_and_speed

__all__ = [
    'PositionViewSet',
]


class PositionViewSet(ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('run',)

    def perform_create(self, serializer):
        distance, speed = calculate_position_distance_and_speed(
            position=Position(**serializer.validated_data),
        )
        position = serializer.save(distance=distance, speed=speed)
        assign_nearby_items_to_user(position)
