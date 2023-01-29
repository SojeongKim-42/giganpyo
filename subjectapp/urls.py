from django.urls import path

from subjectapp.views import TableSubjectViewSets

urlpatterns = [
    # table
    path('', TableSubjectViewSets.as_view({'get': 'list'})),
    path('/<int:subject_id>', TableSubjectViewSets.as_view({'post': 'create', 'delete': 'destroy'}))
]
