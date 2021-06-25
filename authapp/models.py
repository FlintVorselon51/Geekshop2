from datetime import timedelta

from django.db import models
from django.contrib.auth.models import AbstractUser

from django.utils.timezone import now


class ShopUser(AbstractUser):
    avatar = models.ImageField(upload_to='users_avatars', blank=True)
    age = models.PositiveIntegerField(verbose_name='возраст', null=True, blank=True)

    activation_key = models.CharField(max_length=128, blank=True)
    key_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def is_key_expired(self):
        if now() < self.key_created + timedelta(hours=48):
            return False
        return True
