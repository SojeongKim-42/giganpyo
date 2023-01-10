
from parse import *
from django.shortcuts import render, redirect

from timetable.forms import SubjectInfoForm
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
    table = Table.objects.get(id=table_id)
    carts = Cart.objects.filter(table_id=table_id)
    table_subject_list = []
    for cart in carts:
        table_subject_list.append(SubjectInfo.objects.get(id=cart.subject_id))
    context = {'all_subject_list': all_subject_list,
               'table': table, 'table_subject_list': table_subject_list, }
    return render(request, 'timetable/table.html', context)


def add_table_one_subject(request, user_id, table_id, subject_id):

    carts = Cart.objects.filter(table_id=table_id)

    # cart가 비었을 때는 중복 체크 없이 바로 save
    if not carts:
        cart = Cart()
        cart.subject = SubjectInfo.objects.get(id=subject_id)
        cart.table_id = table_id
        cart.save()

    else:
        #중복 체크
        duplication=False
        for cart in carts:
            if subject_id == cart.subject_id:
                duplication = True

        #시간이 겹치는지 확인
        time_overlap=False

        # 추가할 time 가져오기
        subjectTime_to_add_list = SubjectTime.objects.filter(subject_id=subject_id)
        time_to_add_list = []
        for subjectTime_to_add in subjectTime_to_add_list:
            time_to_add_list.append(Time.objects.get(id=subjectTime_to_add.time_id))

        # cart에 담겨 있는 time 모두 가져와 정리하기
        cart_time_list = []
        for cart in carts:
            cart_subjectTime_list = SubjectTime.objects.filter(subject_id=cart.subject_id)
            for subjectTime in cart_subjectTime_list:
                cart_time_list.append(Time.objects.get(id=subjectTime.time_id))

        cart_start_time_list = []
        cart_fin_time_list = []
        for cart_time in cart_time_list:
            start_time = parse("{}:{}", cart_time.start_time)  # ['13', '00']
            start_time = int(start_time[0]+start_time[1])
            cart_start_time_list.append(start_time)

            fin_time = parse("{}:{}", cart_time.fin_time)  # ['14', '30']
            fin_time = int(fin_time[0]+fin_time[1])
            cart_fin_time_list.append(fin_time)

        # 추가할 time과 cart의 time 비교하기
        for time_to_add in time_to_add_list:
            new_st = parse("{}:{}", time_to_add.start_time)
            new_st = int(new_st[0]+new_st[1])
            new_ft = parse("{}:{}", time_to_add.fin_time)
            new_ft = int(new_ft[0]+new_ft[1])
            for old_st, old_ft in cart_start_time_list, cart_fin_time_list:
                if ((new_st>=old_st) and (old_ft>=new_st)) or ((old_st>=new_st) and (new_ft>=old_st)):
                    time_overlap=True
                    break

        # cart에 없는 과목이고 시간이 겹치지 않을 때만 저장
        if (not duplication) and (not time_overlap):
            cart = Cart()
            cart.subject = SubjectInfo.objects.get(id=subject_id)
            cart.table_id = table_id
            cart.save()
    return redirect('timetable:table', user_id=user_id, table_id=table_id)
    
    
def del_table_one_subject(request, user_id, table_id, subject_id):
    cart=Cart.objects.get(subject_id=subject_id, table_id=table_id)
    cart.delete()
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
