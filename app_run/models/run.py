from django.conf import settings
from django.db import models


class Run(models.Model):
    """Stores info about an athlete's run"""
    class Status(models.TextChoices):
        """Run status"""
        INIT = 'init', 'Init'
        IN_PROGRESS = 'in_progress', 'In Progress'
        FINISHED = 'finished', 'Finished'

    created_at = models.DateTimeField(auto_now_add=True)
    athlete = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='runs',
    )
    comment = models.TextField(blank=True)
    status = models.CharField(
        max_length=11,
        choices=Status.choices,
        default=Status.INIT,
    )

    class Meta:
        ordering = ('-created_at',)
