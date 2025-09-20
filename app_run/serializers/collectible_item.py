from rest_framework import serializers

from ..models import CollectibleItem


class CollectibleItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectibleItem
        fields = (
            'name',
            'uid',
            'latitude',
            'longitude',
            'picture',
            'value',
        )

    def validate_latitude(self, value):
        if value < -90 or value > 90:
            raise serializers.ValidationError(
                'Latitude must be between -90 and 90.'
            )
        return value

    def validate_longitude(self, value):
        if value < -180 or value > 180:
            raise serializers.ValidationError(
                'Longitude must be between -180 and 180.'
            )
        return value
