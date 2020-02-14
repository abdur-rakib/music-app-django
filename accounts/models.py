from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

class User(AbstractUser):
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/profile.png', blank=True)

    def get_absolute_url(self):
        return reverse('profile', kwargs={'pk': self.pk})