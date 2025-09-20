from django.db import models


class CollectibleItem(models.Model):
    name = models.TextField()
    uid = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    picture = models.URLField()
    value = models.IntegerField()
