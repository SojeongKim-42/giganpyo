from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from accountapp.managers import CustomUserManager


class User(AbstractUser):
    username = None
    email = models.EmailField('email_address', unique=True)
    is_active = models.BooleanField(default=False)
    student_ID = models.CharField(max_length=20, null=True)
    MAJOR_CHOICES = (
        ('기초', '기초교육학부'),
        ('전컴', '전기전자컴퓨터전공'),
        ('소재', '신소재공학전공'),
        ('기계', '기계공학전공'),
        ('지환', '지구환경공학전공'),
        ('물리', '물리전공'),
        ('화학', '화학전공'),
        ('생명', '생명과학전공'),
    )
    major = models.CharField(max_length=2, choices=MAJOR_CHOICES)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
