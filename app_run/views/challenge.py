from collections import defaultdict

from django.db.models import F, Value
from django.db.models.functions import Concat
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from app_run.models import Challenge
from app_run.serializers.challenge import ChallengeSerializer

__all__ = [
    'ChallengeListView',
    'challenges_summary',
]


class ChallengeListView(ListAPIView):
    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('athlete',)


@api_view(['GET'])
def challenges_summary(request):
    qs = Challenge.objects.all().annotate(
        athlete_full_name=Concat('athlete__first_name', Value(' '), 'athlete__last_name'),
        athlete_username=F('athlete__username'),
    )
    data = defaultdict(list)
    for challenge in qs:
        data[challenge.full_name].append(dict(
            id=challenge.athlete_id,
            full_name=challenge.athlete_full_name,
            username=challenge.athlete_username,
        ))
    output = [
        {'name_to_display': challenge_name, 'athletes': athletes}
        for challenge_name, athletes in data.items()
    ]
    return Response(data=output)
