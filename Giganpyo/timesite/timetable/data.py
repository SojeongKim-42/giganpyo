from timetable.models import SubjectInfo
import re
import pandas as pd
import numpy

# 엑셀파일 받기
Location = 'C:/Users/이주찬/Desktop/rmathing/mop_rm'
# 이거 바꿔줄 필요 있음
File = 'Excel_Timetable.xls'

data_pd = pd.read_excel('{}/{}'.format(Location, File),
                        header=None, index_col=None, names=None)
data_np = pd.DataFrame.to_numpy(data_pd)
time = []

# 시간정보 읽어오기
for i in range(1, len(data_pd)):
    time.append(re.findall("\d+", str(data_pd[11][i])))
for i in range(len(time)):
    time[i] = numpy.array(time[i]).reshape(len(time[i]) // 4, 2, 2)

# 요일정보 읽어오기
day = []
for i in range(1, len(data_pd)):
    day.append(re.compile("[가-힣]+").findall(str(data_pd[11][i])))

# 교수님정보 읽어오기
prof = []
for i in range(1, len(data_pd)):
    prof.append(re.compile("[가-힣]+").findall(str(data_pd[8][i])))

# 과목명 읽어오기
sub = []
for i in range(1, len(data_pd)):
    sub.append(data_pd[5][i])

# 과목코드 읽어오기
code = []
for i in range(1, len(data_pd)):
    code.append(data_pd[4][i])

for i in range(len(data_pd) - 1):
    q = SubjectInfo(name=sub[i], code=code[i])
    if (len(prof[i]) == 1):
        q.professor1 = prof[i][0]
    elif (len(prof[i]) == 2):
        q.professor1 = prof[i][0]
        q.professor2 = prof[i][1]

    if (len(day[i]) == 1):
        q.day1 = day[i][0]
        q.start_time1 = time[i][0][0][0] + ":" + time[i][0][0][1]
        q.finish_time1 = time[i][0][1][0] + ":" + time[i][0][1][1]
        q.start_h1 = int(time[i][0][0][0])
        q.start_m1 = int(time[i][0][0][1])

        q.fin_h1 = int(time[i][0][1][0])
        q.fin_m1 = int(time[i][0][1][1])
        q.count = 1

    elif (len(day[i]) == 2):
        q.day1 = day[i][0]
        q.day2 = day[i][1]
        q.start_time1 = time[i][0][0][0] + ":" + time[i][0][0][1]
        q.start_time2 = time[i][1][0][0] + ":" + time[i][1][0][1]
        q.finish_time1 = time[i][0][1][0] + ":" + time[i][0][1][1]
        q.finish_time2 = time[i][1][1][0] + ":" + time[i][1][1][1]
        q.start_h1 = int(time[i][0][0][0])
        q.start_m1 = int(time[i][0][0][1])
        q.fin_h1 = int(time[i][0][1][0])
        q.fin_m1 = int(time[i][0][1][1])
        q.start_h2 = int(time[i][1][0][0])
        q.start_m2 = int(time[i][1][0][1])
        q.fin_h2 = int(time[i][1][1][0])
        q.fin_m2 = int(time[i][1][1][1])
        q.count = 2

    elif (len(day[i]) == 3):
        q.day1 = day[i][0]
        q.day2 = day[i][1]
        q.day3 = day[i][2]
        q.start_time1 = time[i][0][0][0] + ":" + time[i][0][0][1]
        q.start_time2 = time[i][1][0][0] + ":" + time[i][1][0][1]
        q.start_time3 = time[i][2][0][0] + ":" + time[i][2][0][1]
        q.finish_time1 = time[i][0][1][0] + ":" + time[i][0][1][1]
        q.finish_time2 = time[i][1][1][0] + ":" + time[i][1][1][1]
        q.finish_time3 = time[i][2][1][0] + ":" + time[i][2][1][1]
        q.start_h1 = int(time[i][0][0][0])
        q.start_m1 = int(time[i][0][0][1])
        q.fin_h1 = int(time[i][0][1][0])
        q.fin_m1 = int(time[i][0][1][1])
        q.start_h2 = int(time[i][1][0][0])
        q.start_m2 = int(time[i][1][0][1])
        q.fin_h2 = int(time[i][1][1][0])
        q.fin_m2 = int(time[i][1][1][1])
        q.start_h3 = int(time[i][2][0][0])
        q.start_m3 = int(time[i][2][0][1])
        q.fin_h3 = int(time[i][2][1][0])
        q.fin_m3 = int(time[i][2][1][1])
        q.count = 3

    elif (len(day[i]) == 4):
        q.day1 = day[i][0]
        q.day2 = day[i][1]
        q.day3 = day[i][2]
        q.day4 = day[i][3]
        q.start_time1 = time[i][0][0][0] + ":" + time[i][0][0][1]
        q.start_time2 = time[i][1][0][0] + ":" + time[i][1][0][1]
        q.start_time3 = time[i][2][0][0] + ":" + time[i][2][0][1]
        q.start_time4 = time[i][3][0][0] + ":" + time[i][3][0][1]
        q.finish_time1 = time[i][0][1][0] + ":" + time[i][0][1][1]
        q.finish_time2 = time[i][1][1][0] + ":" + time[i][1][1][1]
        q.finish_time3 = time[i][2][1][0] + ":" + time[i][2][1][1]
        q.finish_time4 = time[i][3][1][0] + ":" + time[i][3][1][1]
        q.start_h1 = int(time[i][0][0][0])
        q.start_m1 = int(time[i][0][0][1])
        q.fin_h1 = int(time[i][0][1][0])
        q.fin_m1 = int(time[i][0][1][1])
        q.start_h2 = int(time[i][1][0][0])
        q.start_m2 = int(time[i][1][0][1])
        q.fin_h2 = int(time[i][1][1][0])
        q.fin_m2 = int(time[i][1][1][1])
        q.start_h3 = int(time[i][2][0][0])
        q.start_m3 = int(time[i][2][0][1])
        q.fin_h3 = int(time[i][2][1][0])
        q.fin_m3 = int(time[i][2][1][1])
        q.start_h4 = int(time[i][3][0][0])
        q.start_m4 = int(time[i][3][0][1])
        q.fin_h4 = int(time[i][3][1][0])
        q.fin_m4 = int(time[i][3][1][1])
        q.count = 4

    q.save()
