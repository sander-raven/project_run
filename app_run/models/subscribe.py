from django.conf import settings
from django.db import models


class Subscribe(models.Model):
    """Stores athletes' subscriptions to coaches"""
    coach = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='subscriptions_from',
    )
    athlete = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='subscriptions_to',
    )

    class Meta:
        unique_together = ('coach', 'athlete')
