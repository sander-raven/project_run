from rest_framework import serializers

from ..models import Position, Run


class PositionSerializer(serializers.ModelSerializer):
    date_time = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S.%f')

    class Meta:
        model = Position
        fields = (
            'run',
            'latitude',
            'longitude',
            'date_time',
            'distance',
            'speed',
        )

    def validate_run(self, run):
        if run.status != Run.Status.IN_PROGRESS:
            raise serializers.ValidationError(
                'Run is not in progress.'
            )
        return run

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
