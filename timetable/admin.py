from django.contrib import admin
from .models import *


class SubjectInfoAdmin(admin.ModelAdmin):
    search_fields = ['name']


admin.site.register(SubjectInfo, SubjectInfoAdmin)
