from django.db import models
from django.contrib.postgres.fields import JSONField


class TimeStampedMixin(models.Model):
    class Meta:
        abstract = True
    db_updated_at = models.DateTimeField(auto_now=True)
    db_created_at = models.DateTimeField(auto_now_add=True)


class Event(TimeStampedMixin):
    class Meta:
        db_table = 'event'

    location = models.TextField(db_index=True)
    event_id = models.TextField(db_index=True)
    name = models.TextField()
    description = models.TextField(null=True)
    start = models.DateTimeField(db_index=True)
    end = models.DateTimeField(db_index=True)
    logo = models.URLField()
    url = models.URLField()

