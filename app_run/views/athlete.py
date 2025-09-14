from django.contrib.auth import get_user_model
from rest_framework import mixins
from rest_framework import status
from rest_framework.generics import GenericAPIView, get_object_or_404

from app_run.models import AthleteInfo
from app_run.serializers import AthleteInfoSerializer

__all__ = [
    'AthleteInfoView',
]

User = get_user_model()


class AthleteInfoView(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    GenericAPIView
):
    queryset = AthleteInfo.objects.all()
    serializer_class = AthleteInfoSerializer
    lookup_field = 'user_id'

    @staticmethod
    def _check_object(user_id: int):
        user = get_object_or_404(User, id=user_id)
        AthleteInfo.objects.get_or_create(user=user)

    def get(self, request, *args, **kwargs):
        self._check_object(kwargs.get('user_id'))
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        self._check_object(kwargs.get('user_id'))
        response = self.update(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            response.status_code = status.HTTP_201_CREATED
        return response
