from django.contrib.auth import get_user_model
from django.db.models import Subquery, OuterRef, Max, Sum, Avg
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from app_run.models import Run

User = get_user_model()

__all__ = [
    'analytics_for_coach',
]


@api_view(['GET'])
def analytics_for_coach(request, coach_id: int) -> Response:
    """Analytics for coach"""
    coach = get_object_or_404(User, pk=coach_id, is_staff=True)
    qs = Run.objects.filter(athlete__subscriptions_to__coach=coach)
    longest_run_user = None
    longest_run_value = None
    total_run_user = None
    total_run_value = None
    speed_avg_user = None
    speed_avg_value = None
    longest_run = (qs.order_by('-distance').values('athlete_id', 'distance')
                   .first())
    if longest_run is not None:
        longest_run_user = longest_run['athlete_id']
        longest_run_value = longest_run['distance']
    total_run = (qs.values('athlete_id').annotate(sum_distance=Sum('distance'))
                 .order_by('-sum_distance').first())
    if total_run is not None:
        total_run_user = total_run['athlete_id']
        total_run_value = total_run['sum_distance']
    speed_avg = (qs.values('athlete_id').annotate(avg_speed=Avg('speed'))
                 .order_by('-avg_speed').first())
    if speed_avg is not None:
        speed_avg_user = speed_avg['athlete_id']
        speed_avg_value = speed_avg['avg_speed']
    results = {
        'longest_run_user': longest_run_user,
        'longest_run_value': longest_run_value,
        'total_run_user': total_run_user,
        'total_run_value': total_run_value,
        'speed_avg_user': speed_avg_user,
        'speed_avg_value': speed_avg_value,
    }
    return Response(data=results)
