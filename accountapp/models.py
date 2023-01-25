from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from accountapp.managers import CustomUserManager


class User(AbstractUser):
    username = None
    email = models.EmailField('email_address', unique=True)
    is_active = models.BooleanField(default=False)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
