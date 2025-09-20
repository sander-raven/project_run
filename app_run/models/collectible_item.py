from django.conf import settings
from django.db import models


class CollectibleItem(models.Model):
    name = models.TextField()
    uid = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    picture = models.URLField()
    value = models.IntegerField()
    users = models.ManyToManyField(
        to=settings.AUTH_USER_MODEL,
        related_name='items',
    )
