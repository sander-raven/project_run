from django.db import models


class Position(models.Model):
    run = models.ForeignKey(
        to='app_run.Run',
        on_delete=models.CASCADE,
        related_name='positions',
    )
    latitude = models.FloatField()
    longitude = models.FloatField()
