from django.db import models

from tableapp.models import Table
# Create your models here.


class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100)
    credit = models.PositiveSmallIntegerField()
    department = models.CharField(max_length=100, null=True)
    is_required = models.CharField(max_length=100, null=True)
    is_major = models.CharField(max_length=100, null=True)
    is_offline = models.CharField(max_length=100, null=True)
    location = models.CharField(max_length=100, null=True)

    year = models.PositiveSmallIntegerField()
    session = models.CharField(max_length=100)
    times = models.ManyToManyField('Time', related_name='sub_time')
    professors = models.ManyToManyField('Professor', related_name='sub_prof')
    select_person = models.PositiveSmallIntegerField(null=True, default=0)

    def __str__(self):
        return self.name


class Professor(models.Model):
    name = models.CharField(max_length=100)


class Time(models.Model):
    day = models.CharField(max_length=1)
    start_time = models.CharField(max_length=100)
    fin_time = models.CharField(max_length=100)

    def __str__(self):
        return self.day + ' ' + self.start_time + ' ~ ' + self.fin_time

    def equals(time, self):
        if (time.day == self.day) and (time.start_time == self.start_time) and (time.fin_time == self.fin_time):
            return True
        else:
            return False


class Cart(models.Model):
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name='cart_subject')
    table = models.ForeignKey(
        Table, on_delete=models.CASCADE,  related_name='cart_table')