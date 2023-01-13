from django.shortcuts import render, get_object_or_404

# Create your views here.
from rest_framework import viewsets
from rest_framework.response import Response
from subjectapp.models import *
from subjectapp.serializers import *

from rest_framework import status



class SubjectViewSets(viewsets.ModelViewSet):
    serializer_class = SubjectSerializer
    lookup_field = 'subject_id'

    def get_queryset(self):
        return Subject.objects.all()

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


    def list(self, request, table_id, *args, **kwargs):
        carts = Cart.objects.filter(table_id=table_id).values_list('subject_id', flat=True)
        queryset=Subject.objects.filter(id__in=carts)
        serializer = SubjectSerializer(queryset, many=True)
        return Response(serializer.data)
    
    
    def create(self, request, table_id, subject_id, *args, **kwargs):
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
                            return Response(status=status.HTTP_400_BAD_REQUEST)
                        elif (adding_time.time.fin_time > cart_time.time.start_time and adding_time.time.fin_time <= cart_time.time.fin_time):
                            return Response(status=status.HTTP_400_BAD_REQUEST)
                    
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

    def destroy(self, request,subject_id,table_id, *args, **kwargs):
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

