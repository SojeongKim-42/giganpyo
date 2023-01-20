from accountapp.models import User
from rest_framework import serializers
from django.core.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status

class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ["email", "password1", "password2"]

    def create(self, validated_data):
        email = validated_data.get('email')
        password1 = validated_data.get('password1')
        user = User(
            email=email
        )
        
        user.set_password(password1)
        user.save()
        return user
    
    def check_password(self, validated_data):
        password1 = validated_data.get("password1")
        password2 = validated_data.get("password2")
        if password1 != password2:
            return False
        return True

