from django import forms
from timetable.models import *


class SubjectInfoForm(forms.ModelForm):
    class Meta:
        model = SubjectInfo  # 사용할 모델
        fields = ['name', 'code', 'department']  # QuestionForm에서 사용할 Question 모델의 속성
        labels={'name': '과목명', 'code':'과목 코드','department':'학과'}