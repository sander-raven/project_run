from rest_framework import serializers

from ..models import Subscribe


class SubscribeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscribe
        fields = (
            'coach',
            'athlete',
            'rating',
        )

    def validate_rating(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError(
                'Rating must be between 1 and 5.'
            )
        return value
