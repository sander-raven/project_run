from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.response import Response

from app_run.models import AthleteInfo
from app_run.serializers import AthleteInfoSerializer

__all__ = [
    'AthleteInfoView',
]

User = get_user_model()


class AthleteInfoView(GenericAPIView):
    queryset = AthleteInfo.objects.all()
    serializer_class = AthleteInfoSerializer
    lookup_url_kwarg = 'user_id'

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs.get('user_id'))
        athlete_info, _ = AthleteInfo.objects.get_or_create(user=user)
        serializer = self.get_serializer(athlete_info)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs.get('user_id'))
        defaults = dict()
        goals = request.POST.get('goals')
        if goals:
            defaults['goals'] = goals
        weight = request.POST.get('weight')
        if weight:
            try:
                weight = int(weight)
            except ValueError:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            if not (0 < weight < 900):
                return Response(status=status.HTTP_400_BAD_REQUEST)
            defaults['weight'] = weight
        athlete_info, _ = AthleteInfo.objects.update_or_create(
            user=user,
            defaults=defaults,
        )
        serializer = self.get_serializer(athlete_info)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
