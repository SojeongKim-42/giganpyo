from accountapp.models import User
from rest_framework import serializers
from django.core.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
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


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    # response 커스텀 
    default_error_messages = {
        'no_active_account': {'message':'username or password is incorrect!', 
                              'success': False,
                              'status' : 401}
    }
    # 유효성 검사
    def validate(self, attrs):
        data = super().validate(attrs)
        
        refresh = self.get_token(self.user)
        
        # response에 추가하고 싶은 key값들 추가
        data['email'] = self.user.email
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['success'] = True
        
        return data
