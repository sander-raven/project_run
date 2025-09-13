from rest_framework import serializers

from ..models import AthleteInfo


class AthleteInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = AthleteInfo
        fields = (
            'goals',
            'weight',
            'user_id',
        )
