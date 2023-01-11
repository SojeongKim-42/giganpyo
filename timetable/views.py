
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


def is_valid_queryparam(param):
    return param != '' and param is not None


def index(request):
    if is_valid_queryparam(request.user.id):
        return redirect('timetable:main', user_id=request.user.id)
    else:
        return redirect('common:login')


def main(request, user_id):
    all_table_list = Table.objects.filter(user_id=request.user.id)
    context = {'all_table_list': all_table_list}
    return render(request, 'timetable/main.html', context)


def table(request, user_id, table_id):
    all_subject_list = SubjectInfo.objects.order_by('name')
    all_subject_time_list = []
    for cnt in range(len(all_subject_list)):
        subject = all_subject_list[cnt]
        time_id_list = SubjectTime.objects.filter(
            subject_id=subject.id).values_list('time_id', flat=True)
        time_list = Time.objects.filter(id__in=time_id_list)
        all_subject_time_list.append([])
        all_subject_time_list[cnt].append(subject)
        all_subject_time_list[cnt].append(time_list)

    table = Table.objects.get(id=table_id)
    carts = Cart.objects.filter(table_id=table_id)
    table_subject_list = []
    for cart in carts:
        table_subject_list.append(SubjectInfo.objects.get(id=cart.subject_id))
        time_id_list = SubjectTime.objects.filter(
            subject_id=subject.id).values_list('time_id', flat=True)

    table_subject_time_list = []
    for cnt in range(len(table_subject_list)):
        subject = table_subject_list[cnt]
        time_id_list = SubjectTime.objects.filter(
            subject_id=subject.id).values_list('time_id', flat=True)
        time_list = Time.objects.filter(id__in=time_id_list)
        table_subject_time_list.append([])
        table_subject_time_list[cnt].append(subject)
        table_subject_time_list[cnt].append(time_list)

    context = {'all_subject_time_list': all_subject_time_list,
               'table': table, 'table_subject_time_list': table_subject_time_list}
    return render(request, 'timetable/table.html', context)


def add_table_one_subject(request, user_id, table_id, subject_id):
    cart_is_not_empty = Cart.objects.filter(table_id=table_id)

    # 카트가 비어있지 않다면 중복 체크
    if cart_is_not_empty:
        adding_times = SubjectTime.objects.filter(subject_id=subject_id)
        cart_subject_ids = Cart.objects.filter(
            table_id=table_id).values_list('subject_id', flat=True)
        cart_times = SubjectTime.objects.filter(
            subject_id__in=cart_subject_ids)

        for adding_time in adding_times:
            for cart_time in cart_times:
                if adding_time.time.day == cart_time.time.day:
                    if (adding_time.time.start_time >= cart_time.time.start_time and adding_time.time.start_time < cart_time.time.fin_time):
                        return HttpResponse("The Subject Time Overlaps")
                    elif (adding_time.time.fin_time > cart_time.time.start_time and adding_time.time.fin_time <= cart_time.time.fin_time):
                        return HttpResponse("The Subject Time Overlaps")

    Cart(subject=SubjectInfo.objects.get(id=subject_id), table_id=table_id).save()

    # 선택한 사람 추가하기: 다른 테이블에 해당 subject가 없다면 +1 (처음 과목 추가하는 경우)
    other_table_ids = Table.objects.filter(user_id=request.user.id).exclude(
        id=table_id).values_list('id', flat=True)
    other_table_subject_ids = SubjectInfo.objects.filter(id__in=Cart.objects.filter(
        table_id__in=other_table_ids).values_list('subject_id', flat=True)).values_list('id', flat=True)
    
    if subject_id not in other_table_subject_ids:
        adding_subject = SubjectInfo.objects.get(id=subject_id)
        adding_subject.select_person += 1
        adding_subject.save()
    return redirect('timetable:table', user_id=user_id, table_id=table_id)


def del_table_one_subject(request, user_id, table_id, subject_id):
    cart = Cart.objects.get(subject_id=subject_id, table_id=table_id)
    cart.delete()

    # 선택한 사람 삭제하기: 다른 테이블에 해당 subject가 없다면 -1 ()
    other_table_ids = Table.objects.filter(user_id=request.user.id).exclude(
        id=table_id).values_list('id', flat=True)
    other_table_subject_ids = SubjectInfo.objects.filter(id__in=Cart.objects.filter(
        table_id__in=other_table_ids).values_list('subject_id', flat=True)).values_list('id', flat=True)

    if subject_id not in other_table_subject_ids:
        adding_subject = SubjectInfo.objects.get(id=subject_id)
        adding_subject.select_person -= 1
        adding_subject.save()

    return redirect('timetable:table', user_id=user_id, table_id=table_id)


def create_table(request, user_id):
    table = Table()
    table.user = User.objects.get(id=request.user.id)
    table.save()
    return redirect('timetable:main', user_id=request.user.id)


def delete_table(request, user_id, table_id):
    table = Table.objects.get(id=table_id)
    table.delete()
    return redirect('timetable:main', user_id=request.user.id)


# API
class SubjectInfoAPI(APIView):
    def get(self, request):
        queryset = SubjectInfo.objects.all()
        print(queryset)
        serializer = SubjectInfoSerializer(queryset, many=True)
        return Response(serializer.data)

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

    # SubjectInfo, subject_prof, subject_time 채우기
    for i in range(len(data_pd) - 1):
        subjectInfo = SubjectInfo(name=names[i], code=codes[i], credit=credits[i], department=departments[i],
                                  is_required=is_requireds[i], is_major=is_majors[i], is_offline=is_offlines[i], year=year, session=session)

        subjectInfo.save()

    for i in range(len(data_pd) - 1):
        subjectInfo = SubjectInfo.objects.get(name=names[i], code=codes[i], credit=credits[i], department=departments[i],
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

