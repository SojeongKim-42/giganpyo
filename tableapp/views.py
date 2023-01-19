from tableapp.models import Table
from django.contrib.auth.models import User

from tableapp.serializers import TableSerializer

from rest_framework import viewsets, status, exceptions
from rest_framework.response import Response

# Create your views here.
class TableViewSets(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    lookup_field='table_id'
    # permission_classes = (IsAuthenticated,)
    
    def list(self, request, user_id, *args, **kwargs):
        if request.user.id != user_id:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "자신의 시간표만 볼 수 있습니다."})
        queryset = self.get_queryset().filter(user_id=user_id)

        # page = self.paginate_queryset(queryset)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, user_id, table_id, *args, **kwargs):
        # 로그인 검증 필요
        if user_id not in User.objects.all().values_list('id', flat=True):
            return Response(status=status.HTTP_404_NOT_FOUND, data={"message": "존재하지 않는 유저입니다."})
        if table_id not in Table.objects.all().values_list('table_id', flat=True):
            return Response(status=status.HTTP_404_NOT_FOUND, data={"message": "존재하지 않는 시간표입니다."})
        try:
            instance = self.queryset.get(table_id=table_id, user_id=request.user.id)
        except Exception:
            return Response(status=status.HTTP_403_FORBIDDEN, data={"message": "자신의 시간표만 수정할 수 있습니다."})
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def create(self, request, user_id, *args, **kwargs):
        if request.user.id != int(request.data['user']):
            return Response(status=status.HTTP_403_FORBIDDEN, data={"message": "자신의 시간표만 수정할 수 있습니다."})
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def update(self, request, user_id, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data={}
        data['user']=user_id
        data['name']=request.data['name']
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
