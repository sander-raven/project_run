from django.conf import settings
from django.db import models
from geopy.distance import geodesic


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
    distance = models.FloatField(blank=True, null=True)
    run_time_seconds = models.PositiveIntegerField(blank=True, null=True)
    speed = models.FloatField(
        null=True,
        blank=True,
        help_text='Average speed. In meters per second.',
    )

    class Meta:
        ordering = ('-created_at',)

    def change_status(
            self,
            new_status: Status,
    ) -> bool:
        """Change run status"""
        if (
                (new_status == self.Status.IN_PROGRESS
                and self.status == self.Status.INIT)
                or (new_status == self.Status.FINISHED
                and self.status == self.Status.IN_PROGRESS)
        ):
            self.status = new_status
            self.save()
            return True
        return False

    def calculate_run_values(self):
        """Calculate run distance, time and average speed"""
        if self.status != self.Status.FINISHED:
            return
        distance = 0.0
        prev_point = None
        for position in self.positions.all():
            point = (position.latitude, position.longitude)
            if prev_point:
                distance += geodesic(prev_point, point).km
            prev_point = point
        self.distance = distance
        values = self.positions.all().aggregate(
            run_time_seconds=models.Max('date_time') - models.Min('date_time'),
            avg_speed=models.Avg('speed'),
        )
        run_time_seconds = values['run_time_seconds']
        if run_time_seconds is not None:
            run_time_seconds = run_time_seconds.total_seconds()
        self.run_time_seconds = run_time_seconds
        self.speed = values['avg_speed']
        self.save()
