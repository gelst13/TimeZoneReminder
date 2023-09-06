import time
from datetime import datetime, timedelta, timezone
from django.db import models
from django.utils import timezone
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.date_posted}  {self.title}'

    @property
    def date_local(self):
        tz = timezone.get_current_timezone()  # get local offset
        return self.date_posted.strftime('%d.%m.%Y %H:%M %z%Z')
