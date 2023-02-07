from django.contrib import admin
from subjectapp.models import *

class SubjectAdmin(admin.ModelAdmin):
    search_fields = ['name', 'code']
    list_display=['subject_id','name','code','select_person']

class CartAdmin(admin.ModelAdmin):
    search_fields = ['subject_id']
    list_display=['id','subject_id','table_id']

class TimeAdmin(admin.ModelAdmin):
    search_fields = ['id','day']
    list_display=['id','day','start_time','fin_time']

class ProfessorAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display=['id','name']

admin.site.register(Subject, SubjectAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Time, TimeAdmin)
admin.site.register(Professor, ProfessorAdmin)

# Register your models here.
