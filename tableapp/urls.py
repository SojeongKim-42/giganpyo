from django.urls import path

from tableapp.views import TableViewSets

urlpatterns = [
    # table
    path('', TableViewSets.as_view({'get': 'list', 'post': 'create'})),
    path('/<int:table_id>',
         TableViewSets.as_view({'patch': 'partial_update', 'delete': 'destroy'})),
]
