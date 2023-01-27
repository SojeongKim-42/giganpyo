from django.http import HttpResponse
from django.shortcuts import render
from subjectapp.models import *
from parse import *

import pandas as pd
import re
import numpy


def data_save():
    # 엑셀파일 받기
    Location = './'
    # 이거 바꿔줄 필요 있음
    File = '23_spring.xls'

    year = 2023
    session = "spring"

    data_pd = pd.read_excel('{}/{}'.format(Location, File),header=None, index_col=None, names=None)

    t_data=data_pd.T
    columns = t_data[0]
    DEPARTMENT = t_data[columns == '개설부서'].index[0]
    CODE = t_data[columns == '교과목-분반'].index[0]
    NAME = t_data[columns == '교과목명'].index[0]
    REQUIRED = t_data[columns == '이수\n구분'].index[0]
    PROFESSOR = t_data[columns == '담당교수'].index[0]
    LEC_EXP_CRE = t_data[columns == '강/실/학'].index[0]
    TIME = t_data[columns == '시간표'].index[0]
    LOCATION = t_data[columns == '강의실'].index[0]
    MAX = t_data[columns == '수강\n정원'].index[0]
    OFFLINE = t_data[columns == '강의\n방법'].index[0]
    MAJOR = t_data[columns == '교과\n연구'].index[0]

    # 시간정보, 요일정보 읽어오기
    times = []
    days = []
    for i in range(1, len(data_pd)):
        times.append(re.findall("\d+", str(data_pd[TIME][i])))
        days.append(re.compile("[가-힣]+").findall(str(data_pd[TIME][i])))

    for i in range(len(times)):
        times[i] = numpy.array(times[i]).reshape(len(times[i]) // 4, 2, 2)

    # Time 중복 제거
    all_times_days = []
    for i in range(len(data_pd)-1):
        for j in range(len(days[i])):
            time = Time(day=days[i][j],
                        start_h=int(times[i][j][0][0]), start_m=int(times[i][j][0][1]),
                        fin_h=int(times[i][j][1][0]), fin_m=int(times[i][j][1][1]),
                        start_time=times[i][j][0][0] + ":" + times[i][j][0][1],
                        fin_time=times[i][j][1][0] + ":" + times[i][j][1][1],)
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
        data_pd[PROFESSOR][i] = str(data_pd[PROFESSOR][i]).replace(" ", "")
        profs.append(re.compile("[가-힣]+").findall(data_pd[PROFESSOR][i]))

    # Prof 중복 제거
    unique_profs = list(set(sum(profs, [])))

    # 과목명, 과목코드, 학점정보, 개설부서, 필수여부, 전공 여부, 대면 비대면, 강의실, 수강정원
    names = []
    codes = []
    credits = []
    departments = []
    is_requireds = []
    is_majors = []
    is_offlines = []
    locations = []
    max_persons = []

    for i in range(1, len(data_pd)):
        names.append(data_pd[NAME][i])
        codes.append(data_pd[CODE][i])
        parsed = parse("{lec}/{exp}/{cre}", str(data_pd[LEC_EXP_CRE][i]))
        credits.append(int(parsed["cre"]))   
        departments.append(data_pd[DEPARTMENT][i])    
        is_requireds.append(data_pd[REQUIRED][i])    
        is_majors.append(data_pd[MAJOR][i])    
        is_offlines.append(data_pd[OFFLINE][i])
        locations.append(data_pd[LOCATION][i])
        max_persons.append(data_pd[MAX][i])

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
                              is_required=is_requireds[i], is_major=is_majors[i], is_offline=is_offlines[i],
                              location=locations[i], max_person=max_persons[i], year=year, session=session)
        subjectInfo.save()

    for i in range(len(data_pd) - 1):

        for j in range(len(profs[i])):
            subjectInfo = Subject.objects.get(name=names[i], code=codes[i], credit=credits[i], department=departments[i],
                                          is_required=is_requireds[i], is_major=is_majors[i], is_offline=is_offlines[i],
                                          location=locations[i],max_person=max_persons[i], year=year, session=session)
            professor = Professor.objects.get(name=profs[i][j])
            subjectInfo.professors.add(professor)
            subjectInfo.save()

        for j in range(len(days[i])):
            subjectInfo = Subject.objects.get(name=names[i], code=codes[i], credit=credits[i], department=departments[i],
                                              is_required=is_requireds[i], is_major=is_majors[i], is_offline=is_offlines[i],
                                              location=locations[i], max_person=max_persons[i], year=year, session=session)
            time = Time.objects.get(day=days[i][j],
                                    start_time=times[i][j][0][0] +
                                    ":" + times[i][j][0][1],
                                    fin_time=times[i][j][1][0] + ":" + times[i][j][1][1])
            subjectInfo.times.add(time)
            subjectInfo.save()

    return HttpResponse("Created")
