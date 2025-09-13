from django.conf import settings
from django.db import models


class AthleteInfo(models.Model):
    """Additional info about the athlete"""
    user = models.OneToOneField(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='athlete_info',
    )
    goals = models.TextField(blank=True)
    weight = models.IntegerField(blank=True, null=True)
