import json
import os
from django.shortcuts import render, get_object_or_404

# Create your views here.
from rest_framework import viewsets, exceptions
from rest_framework.response import Response
from giganpyo import settings
from subjectapp.models import *
# from django.contrib.auth.models import User
from accountapp.models import User
from subjectapp.serializers import *

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.db.models import Q

class SubjectViewSets(viewsets.ModelViewSet):
    serializer_class = SubjectSerializer
    lookup_field = 'subject_id'
    permissions_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def is_valid_queryparam(self, param):
        return param != '' and param is not None

    def is_valid_queryparam(self, param):
        return param != '' and param is not None

    def get_queryset(self):
        return Subject.objects.all()

    # TODO : 정렬! 필터!
    # 많이 담은 순
    # 이름 순
    def list(self, request, *args, **kwargs):
        name = request.GET.get('name')  # 과목이름
        professor = request.GET.get('professor')
        code = request.GET.get('code')  # 과목코드
        day = request.GET.get('day')  # 요일
        time = request.GET.get('time')  # 시간
        department = request.GET.get('department', '기초교육학부')  # 부서
        # TODO : 변수명 sort 대신 order로 변경?
        sort = request.GET.get('sort')  # 정렬기준

        queryset = self.get_queryset()

        if self.is_valid_queryparam(name):
            queryset = queryset.filter(name__icontains=name)
        if self.is_valid_queryparam(professor):
            queryset = queryset.filter(
                professors__name__icontains=professor
            )
        if self.is_valid_queryparam(code):
            queryset = queryset.filter(code__iexact=code)
        if self.is_valid_queryparam(day):
            queryset = queryset.filter(times__day__exact=day)
        if self.is_valid_queryparam(time):
            queryset = queryset.filter(
                times__start_time__exact=time
            )
        if self.is_valid_queryparam(department):
            queryset = queryset.filter(department__exact=department)

        if sort == 'select_desc': #많이 담은 순
            queryset = queryset.order_by('-select_person', 'name')
        elif sort == 'select_asc': #적게 담은 순
            queryset = queryset.order_by('select_person', 'name')
        elif sort == 'code':
            queryset = queryset.order_by('code')
        elif sort == 'name':
            queryset = queryset.order_by('name')
        else:
            queryset = queryset.all()
        queryset = queryset.distinct()

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)
        # with open(os.path.join(settings.BASE_DIR, 'static/subjects.json'), encoding='utf-8') as subjects_file:
        #     subjects_file = json.load(subjects_file)   
        # return Response(subjects_file)


class TableSubjectViewSets(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    lookup_fields=('subject_id', 'table_id')
    permissions_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get_queryset(self):
        return Cart.objects.all()


    def get_object(self):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        filter = {}
        for field in self.lookup_fields:
            try:                                  # Get the result with one or more fields.
                filter[field] = self.kwargs[field]
            except KeyError:
                pass
        return get_object_or_404(queryset, **filter)  # Lookup the object


    def list(self, request, user_id, table_id, *args, **kwargs):
        # if request.auth==None:
            #     return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "유저 정보를 확인할 수 없습니다."})
        if user_id not in User.objects.all().values_list('id', flat=True):
            return Response(status=status.HTTP_404_NOT_FOUND, data={"message": "존재하지 않는 유저입니다."})
        if table_id not in Table.objects.all().values_list('table_id', flat=True):
            return Response(status=status.HTTP_404_NOT_FOUND, data={"message": "존재하지 않는 시간표입니다."})
        if request.user.id != user_id:
            return Response(status=status.HTTP_403_FORBIDDEN, data={"message": "자신의 시간표만 확인할 수 있습니다."})
        try:
            Table.objects.get(table_id=table_id, user_id=request.user.id)
        except Exception:
            return Response(status=status.HTTP_403_FORBIDDEN, data={"message": "해당 유저에게 접근 권한이 없는 시간표입니다."})
        carts = Cart.objects.filter(table_id=table_id).values_list('subject_id', flat=True)
        queryset=Subject.objects.filter(subject_id__in=carts)
        serializer = SubjectSerializer(queryset, many=True)
        return Response(serializer.data)
    
    
    def create(self, request, user_id, table_id, subject_id, *args, **kwargs):
        if request.user.id != user_id:
            return Response(status=status.HTTP_403_FORBIDDEN, data={"message": "자신의 시간표만 수정할 수 있습니다."})
        if user_id not in User.objects.all().values_list('id', flat=True):
            return Response(status=status.HTTP_404_NOT_FOUND, data={"message": "존재하지 않는 유저입니다."})
        carts = Cart.objects.filter(table_id=table_id)
        adding_subject = Subject.objects.get(subject_id=subject_id)


        # 카트가 비어있지 않다면 중복 체크
        if carts:
            adding_times = Time.objects.filter(subject=subject_id)
            cart_subject_ids = Cart.objects.filter(
                table_id=table_id).values_list('subject_id', flat=True)
            cart_times = Time.objects.filter(subject__in=cart_subject_ids)
            
            if subject_id in carts.values_list('subject_id', flat=True):
                name=adding_subject.name
                return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "이미 담은 과목입니다.", "name": name, "id":subject_id })

            for adding_time in adding_times:
                for cart_time in cart_times:
                    if adding_time.day == cart_time.day:
                        old = cart_time.start_time + " ~ " + cart_time.fin_time
                        new = adding_time.start_time + " ~ " + adding_time.fin_time
                        if (adding_time.start_time >= cart_time.start_time and adding_time.start_time < cart_time.fin_time):
                            return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "시간이 겹칩니다.", "old": old, "new": new})
                        elif (adding_time.fin_time > cart_time.start_time and adding_time.fin_time <= cart_time.fin_time):
                            return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "시간이 겹칩니다.", "old": old, "new": new})

        # 선택한 사람 추가하기: 메인테이블일 경우 +1
        if Table.objects.get(table_id=table_id).main:
            adding_subject.select_person+=1
            adding_subject.save()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, table_id, subject_id)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer, table_id, subject_id):
        serializer.save(subject_id=subject_id, table_id=table_id)

    def destroy(self, request, user_id, subject_id,table_id, *args, **kwargs):
        # if request.auth == None:
        #     return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "유저 정보를 확인할 수 없습니다."})
        if request.user.id != user_id:
            return Response(status=status.HTTP_403_FORBIDDEN, data={"message": "자신의 시간표만 수정할 수 있습니다."})
        if user_id not in User.objects.all().values_list('id', flat=True):
            return Response(status=status.HTTP_404_NOT_FOUND, data={"message": "존재하지 않는 유저입니다."})
        if table_id not in Table.objects.all().values_list('table_id', flat=True):
            return Response(status=status.HTTP_404_NOT_FOUND, data={"message": "존재하지 않는 시간표입니다."})
        if subject_id not in Subject.objects.all().values_list('subject_id', flat=True):
            return Response(status=status.HTTP_404_NOT_FOUND, data={"message": "존재하지 않는 과목입니다."})
        if subject_id not in Cart.objects.filter(table_id=table_id).values_list('subject_id', flat=True):
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "장바구니에 담기지 않은 과목입니다."})

        # 선택한 사람 삭제하기: 메인테이블에 담긴 subject면 -1
        if Table.objects.get(table_id=table_id).main:
            deleting_subject = Subject.objects.get(subject_id=subject_id)
            deleting_subject.select_person -= 1
            deleting_subject.save()

        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

