from django.contrib.auth import get_user_model
from django.db.models import Avg
from rest_framework import serializers

from ..helpers import UserTypes
from ..models import Run
from .collectible_item import CollectibleItemSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    runs_finished = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

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
            'rating',
        )

    def get_type(self, obj):
        if obj.is_staff:
            return UserTypes.COACH.value
        else:
            return UserTypes.ATHLETE.value

    def get_runs_finished(self, obj):
        if hasattr(obj, 'runs_finished'):
            return obj.runs_finished
        return obj.runs.filter(status=Run.Status.FINISHED).count()

    def get_rating(self, obj):
        if hasattr(obj, 'rating'):
            return obj.rating
        return obj.subscriptions_from.annotate(avg_rating=Avg('rating'))['avg_rating']

class UserWithItemsSerializer(UserSerializer):
    items = CollectibleItemSerializer(many=True, read_only=True)

    class Meta(UserSerializer.Meta):
        model = User
        fields = UserSerializer.Meta.fields + ('items',)


class UserAthleteSerializer(UserWithItemsSerializer):
    coach = serializers.SerializerMethodField()

    class Meta(UserWithItemsSerializer.Meta):
        model = User
        fields = UserWithItemsSerializer.Meta.fields + ('coach',)

    def get_coach(self, obj):
        coach_ids = obj.subscriptions_to.all().values_list(
            'coach_id', flat=True
        )
        if len(coach_ids) > 0:
            return coach_ids[0]


class UserCoachSerializer(UserWithItemsSerializer):
    athletes = serializers.SerializerMethodField()

    class Meta(UserWithItemsSerializer.Meta):
        model = User
        fields = UserWithItemsSerializer.Meta.fields + ('athletes',)

    def get_athletes(self, obj):
        return obj.subscriptions_from.all().values_list(
            'athlete_id', flat=True
        )
