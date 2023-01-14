from django.shortcuts import render, get_object_or_404

# Create your views here.
from rest_framework import viewsets, exceptions
from rest_framework.response import Response
from subjectapp.models import *
from django.contrib.auth.models import User
from subjectapp.serializers import *

from rest_framework import status


class SubjectViewSets(viewsets.ModelViewSet):
    serializer_class = SubjectSerializer
    lookup_field = 'subject_id'

    def get_queryset(self):
        return Subject.objects.filter(department='기초교육학부')

    def list(self, request, *args, **kwargs):
        
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)         
        return Response(serializer.data)


class TableSubjectViewSets(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    lookup_fields=('subject_id', 'table_id')

    def get_queryset(self):
        return Cart.objects.all()


    def get_object(self):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        filter = {}
        for field in self.lookup_fields:
            try:                                  # Get the result with one or more fields.
                filter[field] = self.kwargs[field]
            except Exception:
                pass
        return get_object_or_404(queryset, **filter)  # Lookup the object


    def list(self, request, user_id, table_id, *args, **kwargs):
        # if request.auth==None:
        #      raise exceptions.ParseError("사용자 정보를 확인할 수 없습니다.")
        if user_id not in User.objects.all().values_list('id', flat=True):
            raise exceptions.ParseError("존재하지 않는 유저입니다.")
        if table_id not in Table.objects.all().values_list('id', flat=True):
            raise exceptions.ParseError("존재하지 않는 시간표입니다.")
        if request.user.id != user_id:
            raise exceptions.PermissionDenied("자신의 시간표만 확인할 수 있습니다.")
        try:
            Table.objects.get(id=table_id, user_id=request.user.id)
        except Exception:
            raise exceptions.PermissionDenied("해당 유저에게 접근 권한이 없는 시간표입니다.")
        carts = Cart.objects.filter(table_id=table_id).values_list('subject_id', flat=True)
        queryset=Subject.objects.filter(id__in=carts)
        serializer = SubjectSerializer(queryset, many=True)
        return Response(serializer.data)
    
    
    def create(self, request, user_id, table_id, subject_id, *args, **kwargs):
        if request.user.id != user_id:
            raise exceptions.PermissionDenied("자신의 시간표만 수정할 수 있습니다.")     
        if user_id not in User.objects.all().values_list('id', flat=True):
            raise exceptions.ParseError("존재하지 않는 유저입니다.")
        carts = Cart.objects.filter(table_id=table_id)

        # 카트가 비어있지 않다면 중복 체크
        if carts:
            adding_times = SubjectTime.objects.filter(subject_id=subject_id)
            cart_subject_ids = Cart.objects.filter(
                table_id=table_id).values_list('subject_id', flat=True)
            cart_times = SubjectTime.objects.filter(
                subject_id__in=cart_subject_ids)
            
            if subject_id in carts.values_list('subject_id', flat=True):
                raise exceptions.ParseError("이미 담은 과목입니다.")

            for adding_time in adding_times:
                for cart_time in cart_times:
                    if adding_time.time.day == cart_time.time.day:
                        if (adding_time.time.start_time >= cart_time.time.start_time and adding_time.time.start_time < cart_time.time.fin_time):
                            raise exceptions.ParseError("시간이 겹칩니다.")
                        elif (adding_time.time.fin_time > cart_time.time.start_time and adding_time.time.fin_time <= cart_time.time.fin_time):
                            raise exceptions.ParseError("시간이 겹칩니다.")
                    
        # 선택한 사람 추가하기: 다른 테이블에 해당 subject가 없다면 +1 (처음 과목 추가하는 경우)
        other_table_ids = Table.objects.filter(user_id=request.user.id).exclude(
            id=table_id).values_list('id', flat=True)
        other_table_subject_ids = Subject.objects.filter(id__in=Cart.objects.filter(
            table_id__in=other_table_ids).values_list('subject_id', flat=True)).values_list('id', flat=True)

        if subject_id not in other_table_subject_ids:
            adding_subject = Subject.objects.get(id=subject_id)
            adding_subject.select_person += 1
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
        #     raise exceptions.ParseError("사용자 정보를 확인할 수 없습니다.")
        if request.user.id != user_id:
            raise exceptions.PermissionDenied("자신의 시간표만 수정할 수 있습니다.")            
        if user_id not in User.objects.all().values_list('id', flat=True):
            raise exceptions.ParseError("존재하지 않는 유저입니다.")
        if table_id not in Table.objects.all().values_list('id', flat=True):
            raise exceptions.ParseError("존재하지 않는 시간표입니다.")
        if subject_id not in Subject.objects.all().values_list('id', flat=True):
            raise exceptions.ParseError("존재하지 않는 과목입니다.")
        if subject_id not in Cart.objects.filter(table_id=table_id).values_list('subject_id', flat=True):
            raise exceptions.ParseError("장바구니에 담기지 않은 과목입니다.")


        # 선택한 사람 삭제하기: 다른 테이블에 해당 subject가 없다면 -1 ()
        other_table_ids = Table.objects.filter(user_id=request.user.id).exclude(
            id=table_id).values_list('id', flat=True)
        other_table_subject_ids = Subject.objects.filter(id__in=Cart.objects.filter(
            table_id__in=other_table_ids).values_list('subject_id', flat=True)).values_list('id', flat=True)

        if subject_id not in other_table_subject_ids:
            adding_subject = Subject.objects.get(id=subject_id)
            adding_subject.select_person -= 1
            adding_subject.save()
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

