from django.contrib.auth import get_user_model
from rest_framework import serializers

from ..helpers import UserTypes
from ..models import Run

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    runs_finished = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'date_joined',
            'username',
            'last_name',
            'first_name',
            'type',
            'runs_finished',
        )

    def get_type(self, obj):
        if obj.is_staff:
            return UserTypes.COACH.value
        else:
            return UserTypes.ATHLETE.value

    def get_runs_finished(self, obj):
        return obj.runs.filter(status=Run.Status.FINISHED).count()
