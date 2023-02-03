from accountapp.models import User
from rest_framework import serializers
from django.core.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import status, exceptions
from rest_framework.exceptions import APIException
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from django.conf import settings
from django.utils.module_loading import import_string
from rest_framework_simplejwt.settings import api_settings
from allauth.socialaccount.models import SocialAccount

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
        'no_account': {'message':'등록된 Email이 없습니다. 다시 한 번 확인해주세요.', 'success': False, 'status' : 401},
        'incorrect_password': {'message':'Password가 올바르지 않습니다. 다시 한 번 확인해주세요.', 'success': False, 'status' : 401},
        'inactive_account': {'message':'Email 인증이 완료되지 않았습니다. Email 인증을 먼저 완료해주세요.', 'success': False, 'status' : 401},
        'social_account': {'message':'소셜 로그인을 통해 가입하셨습니다. 소셜 로그인을 통해 로그인해주세요.', 'success': False, 'status' : 401},
    }
    # 유효성 검사
    def validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            "password": attrs["password"],
        }
        try:
            authenticate_kwargs["request"] = self.context["request"]
        except KeyError:
            pass

        self.user = authenticate(**authenticate_kwargs)
        
        if not api_settings.USER_AUTHENTICATION_RULE(self.user):
            try:
                user = User.objects.get(email=authenticate_kwargs[self.username_field])
            except User.DoesNotExist:
                raise exceptions.AuthenticationFailed(
                    self.error_messages["no_account"],
                    "no_account"
                )
            if user.is_active == False:
                raise exceptions.AuthenticationFailed(
                    self.error_messages["inactive_account"],
                    "inactive_account",
                )
            elif SocialAccount.objects.filter(user=user).exists():
                raise exceptions.AuthenticationFailed(
                    self.error_messages["social_account"],
                    "social_account",
                )
            else:
                raise exceptions.AuthenticationFailed(
                    self.error_messages["incorrect_password"],
                    "incorrect_password",
                )
        
        data = {}
        # try:
        #     data = super().validate(attrs)
        # except exceptions.AuthenticationFailed as e:
        #     raise exceptions.AuthenticationFailed(self.error_messages['no_active_account'])
        
        refresh = self.get_token(self.user)
        
        # response에 추가하고 싶은 key값들 추가
        data['user_id'] = self.user.pk
        data['email'] = self.user.email
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['success'] = True
        
        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)
        
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