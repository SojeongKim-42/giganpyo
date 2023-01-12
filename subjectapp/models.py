from django.db import models

from tableapp.models import Table
# Create your models here.


class Subject(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    code = models.CharField(max_length=100, blank=True, null=True)
    credit = models.PositiveSmallIntegerField(blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    is_required = models.CharField(max_length=100, blank=True, null=True)
    is_major = models.CharField(max_length=100, blank=True, null=True)
    is_offline = models.CharField(max_length=100, blank=True, null=True)

    year = models.PositiveSmallIntegerField(blank=True, null=True)
    session = models.CharField(max_length=100, blank=True, null=True)

    select_person = models.PositiveSmallIntegerField(
        blank=True, null=True, default=0)

    def __str__(self):
        return self.name


class Professor(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)


class Time(models.Model):
    day = models.CharField(max_length=1, blank=True, null=True)
    start_time = models.CharField(max_length=100, blank=True, null=True)
    fin_time = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.day + ' ' + self.start_time + ' ~ ' + self.fin_time

    def equals(time, self):
        if (time.day == self.day) and (time.start_time == self.start_time) and (time.fin_time == self.fin_time):
            return True
        else:
            return False


class Cart(models.Model):
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, blank=True, null=True, related_name='cart_subject')
    table = models.ForeignKey(
        Table, on_delete=models.CASCADE, blank=True, null=True, related_name='cart_table')


class SubjectProf(models.Model):
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, blank=True, null=True, related_name='sub_prof_subject')
    professor = models.ForeignKey(
        Professor, on_delete=models.CASCADE, blank=True, null=True, related_name='sub_prof_professor')


class SubjectTime(models.Model):
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, blank=True, null=True, related_name='sub_time_subject')
    time = models.ForeignKey(
        Time, on_delete=models.CASCADE, blank=True, null=True, related_name='sub_time_time')
