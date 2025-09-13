from rest_framework import serializers

from ..models import Run
from .athlete import AthleteSerializer


class RunSerializer(serializers.ModelSerializer):
    athlete_data = AthleteSerializer(source='athlete', read_only=True)

    class Meta:
        model = Run
        fields = '__all__'
