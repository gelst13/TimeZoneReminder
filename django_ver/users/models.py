from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Contact(models.Model):
    # id = models.IntegerField(primary_key=True)
    contact_name = models.CharField(max_length=100)
    platform = models.CharField(max_length=20)
    comment = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    zone_name = models.CharField(max_length=100)
    utc_offset = models.FloatField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __repr__(self):
        return '<Contact {} from {}>'.format(self.contact_name,
                                             self.location)

    def get_absolute_url(self):
        return reverse('contact-detail', kwargs={'pk': self.pk})
