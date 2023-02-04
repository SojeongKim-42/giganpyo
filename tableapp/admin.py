from django.contrib import admin
from tableapp.models import Table


class TableAdmin(admin.ModelAdmin):
    search_fields = ['user_id']
    list_display=['table_id','user_id','main','name']

admin.site.register(Table, TableAdmin)
# Register your models here.
