from django.conf import settings
from django.db import models


class Run(models.Model):
    """Stores info about an athlete's run"""
    created_at = models.DateTimeField(auto_now_add=True)
    athlete = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='runs',
    )
    comment = models.TextField(blank=True)

    class Meta:
        ordering = ('-created_at',)
