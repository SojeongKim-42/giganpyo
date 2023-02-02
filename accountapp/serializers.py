from accountapp.models import User
from rest_framework import serializers
from django.core.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import status
from django.conf import settings
from django.utils.module_loading import import_string


class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ["email", "password1", "password2", "student_ID", "major"]

    def create(self, validated_data):
        email = validated_data.get('email')
        password1 = validated_data.get('password1')
        student_ID=validated_data.get('student_ID')
        major=validated_data.get('major')
        user = User(
            email=email,
            student_ID=student_ID,
            major=major,
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
        'no_active_account': {'message':'username or password is incorrect. Or user may not be active - check email.', 
                              'success': False,
                              'status' : 401}
    }
    # 유효성 검사
    def validate(self, attrs):
        data = super().validate(attrs)
        
        refresh = self.get_token(self.user)
        
        # response에 추가하고 싶은 key값들 추가
        data['user_id'] = self.user.pk
        data['email'] = self.user.email
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['success'] = True
        
        return data

class JWTCustomSerializer(serializers.Serializer):
    """
    Serializer for JWT authentication.
    """
    access = serializers.CharField()
    refresh = serializers.CharField()
    user_id = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    def get_user_id(self, obj):
        """
        Required to allow using custom USER_DETAILS_SERIALIZER in
        JWTSerializer. Defining it here to avoid circular imports
        """
        rest_auth_serializers = getattr(settings, 'REST_AUTH_SERIALIZERS', {})

        JWTUserDetailsSerializer = import_string(
            rest_auth_serializers.get(
                'USER_DETAILS_SERIALIZER',
                'dj_rest_auth.serializers.UserDetailsSerializer',
            ),
        )

        user_data = JWTUserDetailsSerializer(obj['user'], context=self.context).data
        return user_data.get("pk")
    
    def get_email(self, obj):
        """
        Required to allow using custom USER_DETAILS_SERIALIZER in
        JWTSerializer. Defining it here to avoid circular imports
        """
        rest_auth_serializers = getattr(settings, 'REST_AUTH_SERIALIZERS', {})

        JWTUserDetailsSerializer = import_string(
            rest_auth_serializers.get(
                'USER_DETAILS_SERIALIZER',
                'dj_rest_auth.serializers.UserDetailsSerializer',
            ),
        )

        user_data = JWTUserDetailsSerializer(obj['user'], context=self.context).data
        return user_data.get("email")

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["student_ID", "major"]

    def update(self, instance, validated_data):
        instance.student_ID = validated_data.get('student_ID', instance.student_ID)
        instance.major = validated_data.get('major', instance.major)
        instance.save()
        return instance