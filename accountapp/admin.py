from django.contrib import admin
from accountapp.models import User


class UserAdmin(admin.ModelAdmin):
    search_fields = ['id', 'email']
    list_display=['id', 'email','is_active']

admin.site.register(User, UserAdmin)
# Register your models here.
