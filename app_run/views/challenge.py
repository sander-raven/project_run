from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView

from app_run.models import Challenge
from app_run.serializers.challenge import ChallengeSerializer

__all__ = [
    'ChallengeListView',
]


class ChallengeListView(ListAPIView):
    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('athlete',)
