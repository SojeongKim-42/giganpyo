from django.shortcuts import render
from tableapp.models import Table
from tableapp.serializers import TableSerializer

from rest_framework import viewsets
from rest_framework.response import Response

# Create your views here.
class TableViewSets(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    # permission_classes = (IsAuthenticated,)
    lookup_field = 'id'
    
    def list(self, request, user_id, *args, **kwargs):
        queryset = self.get_queryset().filter(user_id=user_id)

        # page = self.paginate_queryset(queryset)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    # def get_queryset(self):
    #     return Table.objects.filter(user=self.request.user.id)
    
    