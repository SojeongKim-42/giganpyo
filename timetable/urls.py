from django.urls import path

from . import views

app_name = 'timetable'


urlpatterns = [
    path('<int:user_id>/', views.main, name='main'),
    path('<int:user_id>/table/<table_id>/subject/',
         views.getTableAllSubjects, name='get_table_all_subjects'),
    path('<int:user_id>/table/<table_id>/subject/<int:subject_id>',
         views.addTableOneSubject, name='add_table_one_subject'),
    path('<int:user_id>/table', views.create_table, name='create_table')
    # path('<int:subject_id>/', views.detail, name='detail'),
    # path('data', views.data_save, name='data_save')
]
