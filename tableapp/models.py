from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Table(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name='table_user')
    name = models.CharField(max_length=100, blank=True, null=True)