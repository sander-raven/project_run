from django.contrib.auth import get_user_model
from django.db import IntegrityError
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from app_run.models import Subscribe

User = get_user_model()

__all__ = [
    'subscribe_to_coach',
]


@api_view(['POST'])
def subscribe_to_coach(request, coach_id: int) -> Response:
    """Subscribe athlete to coach"""
    coach = User.objects.filter(pk=coach_id, is_staff=True).first()
    if coach is None:
        return Response(status=status.HTTP_404_NOT_FOUND)
    athlete_id = request.data.get('athlete')
    athlete = User.objects.filter(pk=athlete_id, is_staff=False).first()
    if athlete is None:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    try:
        Subscribe.objects.create(coach=coach, athlete=athlete)
    except IntegrityError:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response()
