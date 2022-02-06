from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class SubjectInfo(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    code = models.CharField(max_length=100, blank=True, null=True)
    professor1 = models.CharField(max_length=100, blank=True, null=True)
    professor2 = models.CharField(max_length=100, blank=True, null=True)

    day1 = models.CharField(max_length=1, blank=True, null=True)
    day2 = models.CharField(max_length=1, blank=True, null=True)
    day3 = models.CharField(max_length=1, blank=True, null=True)
    day4 = models.CharField(max_length=1, blank=True, null=True)

    start_h1 = models.PositiveSmallIntegerField(blank=True, null=True)
    start_m1 = models.PositiveSmallIntegerField(blank=True, null=True)
    fin_h1 = models.PositiveSmallIntegerField(blank=True, null=True)
    fin_m1 = models.PositiveSmallIntegerField(blank=True, null=True)

    start_h2 = models.PositiveSmallIntegerField(blank=True, null=True)
    start_m2 = models.PositiveSmallIntegerField(blank=True, null=True)
    fin_h2 = models.PositiveSmallIntegerField(blank=True, null=True)
    fin_m2 = models.PositiveSmallIntegerField(blank=True, null=True)

    start_m3 = models.PositiveSmallIntegerField(blank=True, null=True)
    start_h3 = models.PositiveSmallIntegerField(blank=True, null=True)
    fin_h3 = models.PositiveSmallIntegerField(blank=True, null=True)
    fin_m3 = models.PositiveSmallIntegerField(blank=True, null=True)

    start_h4 = models.PositiveSmallIntegerField(blank=True, null=True)
    start_m4 = models.PositiveSmallIntegerField(blank=True, null=True)
    fin_h4 = models.PositiveSmallIntegerField(blank=True, null=True)
    fin_m4 = models.PositiveSmallIntegerField(blank=True, null=True)

    start_time1 = models.CharField(max_length=100, blank=True, null=True)
    start_time2 = models.CharField(max_length=100, blank=True, null=True)
    start_time3 = models.CharField(max_length=100, blank=True, null=True)
    start_time4 = models.CharField(max_length=100, blank=True, null=True)
    finish_time1 = models.CharField(max_length=100, blank=True, null=True)
    finish_time2 = models.CharField(max_length=100, blank=True, null=True)
    finish_time3 = models.CharField(max_length=100, blank=True, null=True)
    finish_time4 = models.CharField(max_length=100, blank=True, null=True)

    count = models.PositiveSmallIntegerField(blank=True, null=True)
    credit = models.PositiveSmallIntegerField(blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    is_required = models.CharField(max_length=100, blank=True, null=True)
    is_major = models.CharField(max_length=100, blank=True, null=True)

    year = models.PositiveSmallIntegerField(blank=True, null=True)
    session = models.CharField(max_length=100, blank=True, null=True)

    select_person = models.PositiveSmallIntegerField(blank=True, null=True, default=0)

    def __str__(self):
        return self.name


#
# class User_Info(models.Model):
#     name = models.ForeignKey(User, on_delete=models.CASCADE, null = True)

class Subject_add(models.Model):
    # name = models.CharField(max_length=100)
    subject_add = models.ForeignKey(SubjectInfo, blank=True, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='user_add')


class Evaluation(models.Model):
    subject = models.ForeignKey(SubjectInfo, blank=True, null=True, on_delete=models.CASCADE)
    test = models.PositiveSmallIntegerField(blank=True, null=True)
    assignment = models.PositiveSmallIntegerField(blank=True, null=True)
    grade = models.PositiveSmallIntegerField(blank=True, null=True)
    comment = models.CharField(max_length=100, blank=True, null=True)


class SubjectEval(models.Model):
    subject = models.ForeignKey(SubjectInfo, blank=True, null=True, on_delete=models.CASCADE)
    evaluation = models.ForeignKey(Evaluation, blank=True, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
