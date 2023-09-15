import time
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
from django.db import models
from django.utils import timezone
from django.urls import reverse
from dateutil.tz import tzoffset, tzlocal, tz


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.date_posted}  {self.title}'

    @property
    def date_admin(self):
        return self.date_posted.astimezone(ZoneInfo("Europe/Moscow")).strftime('%d.%m.%Y %H:%M %z%Z')
