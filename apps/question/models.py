from django.db import models
from django.contrib.postgres.fields import JSONField


class Event(models.Model):
    class Meta:
        db_table = 'event'

    name = models.TextField()
    details = JSONField(default={})
