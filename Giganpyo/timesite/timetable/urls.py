from django.urls import path
from . import views

app_name = 'timetable'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:user_id>/', views.mytable, name='mytable'),
    path('add/<int:subject_id>/', views.add, name='add'),
    path('del/<int:subject_id>/', views.delete, name='del'),
    path('eval_add/<int:subject_id>/', views.eval_add, name='eval_add'),
    path('eval_del/<int:subject_id>/', views.eval_del, name='eval_del'),
    # path('data/',views.data_save, name = 'data_save'),
]
