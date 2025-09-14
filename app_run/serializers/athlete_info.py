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

    def validate_weight(self, value):
        if not (0 < value < 900):
            raise serializers.ValidationError(
                'The weight must be in the range of 1 to 899 inclusive.'
            )
