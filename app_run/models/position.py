from django.db import models


class Position(models.Model):
    run = models.ForeignKey(
        to='app_run.Run',
        on_delete=models.CASCADE,
        related_name='positions',
    )
    latitude = models.FloatField()
    longitude = models.FloatField()
    date_time = models.DateTimeField(
        null=True,
        blank=True,
    )
    speed = models.FloatField(
        null=True,
        blank=True,
        help_text=(
            'Speed relative to the previous position, '
            'based on time and distance traveled. In meters per second.'
        ),
    )
    distance = models.FloatField(
        null=True,
        blank=True,
        help_text='Accumulative total of distances traveled. In kilometers.',
    )
