from django.urls import path

from subjectapp.views import SubjectViewSets, TableSubjectViewSets

urlpatterns = [
    # table
    path('subjects/', SubjectViewSets.as_view({'get': 'list'})),
    path('', TableSubjectViewSets.as_view({'get': 'list'})),
    path('<int:subject_id>/', TableSubjectViewSets.as_view({'post': 'create', 'delete': 'destroy'})),
]
