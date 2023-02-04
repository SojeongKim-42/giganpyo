from django.contrib import admin
from subjectapp.models import Subject, Cart

class SubjectAdmin(admin.ModelAdmin):
    search_fields = ['name', 'code']
    list_display=['subject_id','name','code','select_person']

class CartAdmin(admin.ModelAdmin):
    search_fields = ['table_id']
    list_display=['id','subject_id','table_id']

admin.site.register(Subject, SubjectAdmin)
admin.site.register(Cart, CartAdmin)

# Register your models here.
