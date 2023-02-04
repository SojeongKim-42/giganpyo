from django.db import models
from django.core.cache import cache

from tableapp.models import Table
# Create your models here.

class Professor(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

class Time(models.Model):
    id = models.AutoField(primary_key=True)
    day = models.CharField(max_length=1)
    start_time = models.CharField(max_length=100)
    start_h=models.PositiveSmallIntegerField(null=True)
    start_m=models.PositiveSmallIntegerField(null=True)
    fin_time = models.CharField(max_length=100)
    fin_h = models.PositiveSmallIntegerField(null=True)
    fin_m = models.PositiveSmallIntegerField(null=True)

    def __str__(self):
        return self.day + ' ' + self.start_time + ' ~ ' + self.fin_time

    def equals(time, self):
        if (time.day == self.day) and (time.start_time == self.start_time) and (time.fin_time == self.fin_time):
            return True
        else:
            return False

class Subject(models.Model):
    subject_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100)
    credit = models.PositiveSmallIntegerField()
    department = models.CharField(max_length=100, null=True)
    is_required = models.CharField(max_length=100, null=True)
    is_major = models.CharField(max_length=100, null=True)
    is_offline = models.CharField(max_length=100, null=True)
    location = models.CharField(max_length=100, null=True)
    max_person = models.PositiveSmallIntegerField(null=True)
    times = models.ManyToManyField(Time, blank=True)
    professors = models.ManyToManyField(Professor, blank=True)

    year = models.PositiveSmallIntegerField()
    session = models.CharField(max_length=100)
    select_person = models.PositiveSmallIntegerField(null=True, default=0)

    def __str__(self):
        return self.name
    
    # def save(self, *args, **kwargs):
    #     cache.delete('subjects')
    #     super().save(*args, **kwargs)

    # def delete(self, *args, **kwargs):
    #     cache.delete('subjects')
    #     super().delete(*args, **kwargs)

class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name='cart_subject', db_column='subject_id')
    table = models.ForeignKey(
        Table, on_delete=models.CASCADE,  related_name='cart_table')

