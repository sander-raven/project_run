from django.contrib.auth import get_user_model
from rest_framework import serializers

from ..helpers import UserTypes

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'date_joined',
            'username',
            'last_name',
            'first_name',
            'type',
        )

    def get_type(self, obj):
        if obj.is_staff:
            return UserTypes.COACH.value
        else:
            return UserTypes.ATHLETE.value
