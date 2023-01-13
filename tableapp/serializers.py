from rest_framework import serializers
from django.contrib.auth.models import User
from tableapp.models import Table

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password', 'username', 'email', 'first_name', 'last_name']

class TableSerializer(serializers.ModelSerializer):
    user_info = UserSerializer(read_only=True)
    # custom = serializers.SerializerMethodField()

    # def get_custom(self, obj):
    #     obj_id = obj.user.username
    #     # return obj.start_time + "~" + obj.end_time
    #     return f'custom_{obj_id}'
    
    """
    Time
    {
        start_time : "09:00",
        end_time : "10:00"
    }
    """
    class Meta:
        model = Table
        fields = '__all__'