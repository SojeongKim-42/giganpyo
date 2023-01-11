from django.urls import include, path

from . import views

app_name = 'timetable'


urlpatterns = [
     path('<int:user_id>/', views.main, name='main'),
     # table
#     path('<int:user_id>/table', views.create_table, name='create_table'),
#     path('<int:user_id>/table/<table_id>/',
#          views.delete_table, name='delete_table'),
     path('<int:user_id>/table/<table_id>/subject/',
          views.table, name='table'),
     path('<int:user_id>/table/<table_id>/subject/<int:subject_id>',
          views.add_table_one_subject,
          name='add_table_one_subject'),
     path('<int:user_id>/table/<table_id>/subject/<int:subject_id>/del',
          views.del_table_one_subject,
          name='del_table_one_subject')
    # path('data', views.data_save, name='data_save')
]
