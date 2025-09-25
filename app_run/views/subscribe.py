from django.contrib.auth import get_user_model
from django.db import IntegrityError
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from app_run.models import Subscribe
from app_run.serializers.subscribe import SubscribeSerializer

User = get_user_model()

__all__ = [
    'subscribe_to_coach',
    'rate_coach',
]


def get_coach(coach_id: int) -> User | None:
    """Get coach"""
    coach = get_object_or_404(User, pk=coach_id)
    if coach.is_staff:
        return coach


def get_athlete(athlete_id: int) -> User | None:
    """Get athlete"""
    return User.objects.filter(pk=athlete_id, is_staff=False).first()


@api_view(['POST'])
def subscribe_to_coach(request, coach_id: int) -> Response:
    """Subscribe athlete to coach"""
    coach = get_coach(coach_id=coach_id)
    if coach is None:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    athlete = get_athlete(athlete_id=request.data.get('athlete'))
    if athlete is None:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    try:
        Subscribe.objects.create(coach=coach, athlete=athlete)
    except IntegrityError:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    return Response()


@api_view(['POST'])
def rate_coach(request, coach_id: int) -> Response:
    """Rate coach"""
    coach = get_coach(coach_id=coach_id)
    if coach is None:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    athlete = get_athlete(athlete_id=request.data.get('athlete'))
    if athlete is None:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    subscribe = get_object_or_404(Subscribe, coach=coach, athlete=athlete)
    serializer = SubscribeSerializer(
        subscribe, data={'rating': request.data.get('rating')}, partial=True
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response()
