
from parse import *
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *

from .models import *
import pandas as pd
import re
import numpy
from tableapp.models import *
from subjectapp.models import *


# def is_valid_queryparam(param):
#     return param != '' and param is not None


# def index(request):
#     if is_valid_queryparam(request.user.id):
#         return redirect('timetable:main', user_id=request.user.id)
#     else:
#         return redirect('common:login')


# def main(request, user_id):
#     all_table_list = Table.objects.filter(user_id=request.user.id)
#     context = {'all_table_list': all_table_list}
#     return render(request, 'timetable/main.html', context)

# # API


# class SubjectAPI(APIView):
#     def get(self, request):
#         queryset = Subject.objects.all()
#         print(queryset)
#         serializer = SubjectSerializer(queryset, many=True)
#         return Response(serializer.data)

# 과목 저장


def data_save(request):
    # 엑셀파일 받기
    Location = 'C:/Users/pc/Desktop/Giganpyo_new'
    # 이거 바꿔줄 필요 있음
    File = '22_fall.xls'

    year = 2022
    session = "fall"

    data_pd = pd.read_excel('{}/{}'.format(Location, File),
                            header=None, index_col=None, names=None)

    # 시간정보 읽어오기
    times = []
    for i in range(1, len(data_pd)):
        times.append(re.findall("\d+", str(data_pd[13][i])))
    for i in range(len(times)):
        times[i] = numpy.array(times[i]).reshape(len(times[i]) // 4, 2, 2)

    # 요일정보 읽어오기
    days = []
    for i in range(1, len(data_pd)):
        days.append(re.compile("[가-힣]+").findall(str(data_pd[13][i])))

    # Time 중복 제거
    all_times_days = []
    for i in range(len(data_pd)-1):
        for j in range(len(days[i])):
            time = Time(day=days[i][j],
                        start_time=times[i][j][0][0] + ":" + times[i][j][0][1],
                        fin_time=times[i][j][1][0] + ":" + times[i][j][1][1])
            all_times_days.append(time)

    unique_times = []
    for t in all_times_days:
        in_unique = False
        for u in unique_times:
            if t.equals(u):
                in_unique = True
        if not in_unique:
            unique_times.append(t)

    # 교수님정보 읽어오기
    profs = []
    for i in range(1, len(data_pd)):
        data_pd[9][i] = str(data_pd[9][i]).replace(" ", "")
        profs.append(re.compile("[가-힣]+").findall(data_pd[9][i]))

    # Prof 중복 제거
    unique_profs = list(set(sum(profs, [])))

    # 과목명 읽어오기
    names = []
    for i in range(1, len(data_pd)):
        names.append(data_pd[5][i])

    # 과목코드 읽어오기
    codes = []
    for i in range(1, len(data_pd)):
        codes.append(data_pd[4][i])

    # 학점정보 읽어오기
    credits = []
    for i in range(1, len(data_pd)):
        credits.append(int(data_pd[30][i]))

    # 개설부서 읽어오기
    departments = []
    for i in range(1, len(data_pd)):
        departments.append(data_pd[3][i])

    # 필수여부 읽어오기
    is_requireds = []
    for i in range(1, len(data_pd)):
        is_requireds.append(data_pd[6][i])

    # 교양, 전공 읽어오기
    is_majors = []
    for i in range(1, len(data_pd)):
        is_majors.append(data_pd[8][i])

    # 대면, 비대면 읽어오기
    is_offlines = []
    for i in range(1, len(data_pd)):
        is_offlines.append(data_pd[26][i])

    # Professor 채우기
    for i in range(len(unique_profs)):
        professor = Professor(name=unique_profs[i])
        professor.save()

    # Time 채우기
    for i in range(len(unique_times)):
        unique_times[i].save()

    # Subject, subject_prof, subject_time 채우기
    for i in range(len(data_pd) - 1):
        subjectInfo = Subject(name=names[i], code=codes[i], credit=credits[i], department=departments[i],
                              is_required=is_requireds[i], is_major=is_majors[i], is_offline=is_offlines[i], year=year, session=session)

        subjectInfo.save()

    for i in range(len(data_pd) - 1):
        subjectInfo = Subject.objects.get(name=names[i], code=codes[i], credit=credits[i], department=departments[i],
                                          is_required=is_requireds[i], is_major=is_majors[i], is_offline=is_offlines[i],
                                          year=year, session=session)

        for j in range(len(profs[i])):
            professor = Professor.objects.get(name=profs[i][j])
            subject_prof = SubjectProf(
                subject=subjectInfo, professor=professor)
            subject_prof.save()

        for j in range(len(days[i])):
            time = Time.objects.get(day=days[i][j],
                                    start_time=times[i][j][0][0] +
                                    ":" + times[i][j][0][1],
                                    fin_time=times[i][j][1][0] + ":" + times[i][j][1][1])
            subject_time = SubjectTime(subject=subjectInfo, time=time)
            subject_time.save()

    return render(request, 'timetable/subject_list.html')
