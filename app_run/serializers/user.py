from django.contrib.auth import get_user_model
from rest_framework import serializers

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
            return 'coach'
        else:
            return 'athlete'
