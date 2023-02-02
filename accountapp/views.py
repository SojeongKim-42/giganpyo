from base64 import urlsafe_b64decode, urlsafe_b64encode
import json
from tokenize import TokenError
from django.http import JsonResponse
from django.utils.encoding import force_str, force_bytes
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect
from django.db import transaction

import jwt

from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
import requests
from accountapp.tasks import send_verification_email
from accountapp.text import message
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.providers.google import views as google_view
from dj_rest_auth.serializers import TokenSerializer
# TODO setting 바꾸기
from giganpyo.settings import base as settings

from giganpyo.settings.base import SECRET_KEY
from accountapp.models import User
from accountapp.serializers import JWTCustomSerializer, MyTokenObtainPairSerializer, RegisterSerializer
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, viewsets, permissions

from tableapp.models import Table
from accountapp import errors as AccountErrors

from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.account.adapter import get_adapter
from dj_rest_auth.utils import jwt_encode
from dj_rest_auth.jwt_auth import set_jwt_cookies
from dj_rest_auth.app_settings import create_token
from dj_rest_auth.models import get_token_model

#로그인
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            
            refresh_token = serializer.data.get("refresh")
            access_token = serializer.data.get("access")
            
            res = Response(
                serializer.validated_data,
                status=status.HTTP_200_OK,
            )
            # 배포할 때는 httponly=True, secure=True, samesite=Nonee
            # 크롬 정책
            print(access_token)
            res.set_cookie("access", serializer.validated_data.get("access"), httponly=True, secure=True, samesite="None")
            res.set_cookie("refresh", serializer.validated_data.get("refresh"), httponly=True, secure=True, samesite="None")
            print(res.cookies.get("access"))
            return res
        except TokenError as e:
            raise jwt.InvalidTokenError(e.args[0])

# 회원가입
class RegisterAPIView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            if not serializer.check_password(validated_data=serializer.validated_data):
                return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "Passwords don't match"})
            with transaction.atomic():
                user = serializer.save(is_active=False)
                Table.objects.create(user=user, main=True)
            
            domain = getattr(settings, "BASE_URL", "https://www.giganpyo.com")
            # uidb64          = urlsafe_b64encode(bytes(str(user.pk), 'UTF-8')).encode('UTF-8')
            uidb64          = user.id

            token           = jwt.encode({'user':user.id}, SECRET_KEY, algorithm='HS256')
            message_data    = message(domain, uidb64, token)
            mail_title      = "이메일 인증을 완료해주세요"
            
            send_verification_email.apply_async(args=(mail_title, message_data, request.data["email"]))

            return Response({"message": "register successs. Please check your email.", "user_id": user.id}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Activate(APIView):
    def get(self, request, uidb64, token):
        try:
            uid = uidb64
            user = User.objects.get(id=uid)
            user_dic = jwt.decode(token, SECRET_KEY, algorithms='HS256')
            if user.id == user_dic["user"]:
                user.is_active = True
                user.save()
                res = Response(
                    {
                        "message": "email_verify successs"
                    },
                    status=status.HTTP_200_OK,
                )
                return res

            return Response({'message':'auth fail'}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError:
            return Response({'message':'type_error'}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({'message':'INVALID_KEY'}, status=status.HTTP_400_BAD_REQUEST)
        
class EmailResend(APIView):
    def post(self, request):
        try:
            email           = request.data["email"]
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'message':'유효하지 않은 이메일입니다.'}, status=status.HTTP_400_BAD_REQUEST)
            if user.is_active:
                return Response({'message':'이미 인증된 이메일입니다.'}, status=status.HTTP_400_BAD_REQUEST)
                
            domain          = getattr(settings, "BASE_URL", "https://www.giganpyo.com")
            # uidb64          = urlsafe_b64encode(bytes(str(user.pk), 'UTF-8')).encode('UTF-8')
            uidb64          = user.id
            token           = jwt.encode({'user':uidb64}, SECRET_KEY, algorithm='HS256')
            message_data    = message(domain, uidb64, token)
            mail_title      = "이메일 인증을 완료해주세요"
        
            send_verification_email.apply_async(args=(mail_title, message_data, email))
            return Response({"message": "register successs. Please check your email.", "user_id": uidb64}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"message": "email resend fail"}, status=status.HTTP_400_BAD_REQUEST)
"""
Google Login
"""
social_provider_translation = {"google": "구글", "kakao": "카카오"}
BASE_URL = getattr(settings, "BASE_URL")
GOOGLE_CALLBACK_URI = BASE_URL + '/api/user/google/login'

# def google_redirect(request):
#     """
#     Code Request
#     """
#     scope = "https://www.googleapis.com/auth/userinfo.email"
#     client_id = getattr(settings, "SOCIAL_AUTH_GOOGLE_CLIENT_ID")
#     return redirect(f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&response_type=code&redirect_uri={GOOGLE_CALLBACK_URI}&scope={scope}")

@api_view(['GET'])
def google_login(request):
    client_id = getattr(settings, "SOCIAL_AUTH_GOOGLE_CLIENT_ID")
    client_secret = getattr(settings, "SOCIAL_AUTH_GOOGLE_SECRET")

    # code = request.data.get('code')
    code = request.GET.get('code')
    """
    Access Token Request
    """
    token_req = requests.post(
        f"https://oauth2.googleapis.com/token?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code&redirect_uri={GOOGLE_CALLBACK_URI}")

    token_req_json = token_req.json()
    error = token_req_json.get("error")
    if error is not None:
        return AccountErrors.SocialLoginFailed(400, social_provider="구글")
    access_token = token_req_json.get('access_token')
    """
    Email Request
    """
    email_req = requests.get(f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}")
    email_req_status = email_req.status_code
    if email_req_status != 200:
        return AccountErrors.SocialLoginFailed(email_req_status, social_provider="구글")
    email_req_json = email_req.json()
    email = email_req_json.get('email')
    print(email)
    """
    Signup or Signin Request
    """
    # Signin Request
    try:
        user = User.objects.get(email=email)
        # 기존에 가입된 유저의 Provider가 google이 아니면 에러 발생, 맞으면 로그인
        # 다른 SNS로 가입된 유저
        social_user = SocialAccount.objects.get(user=user)
        if social_user is None:
            return AccountErrors.UserAlreadyExist(400, email, social_provider="이메일")
        if social_user.provider != 'google':
            return AccountErrors.UserAlreadyExist(400, email, social_provider=social_provider_translation.get(social_user.provider))
        # 기존에 Google로 가입된 유저
        data = {'access_token': access_token, 'code': code}
        # TODO 이거 바꾸기 (local : 127.0.0.1:8000)
        accept = requests.post(f"http://0.0.0.0:8000/api/user/google/login/finish", data=data)
        print(accept)
        accept_status = accept.status_code
        if accept_status != 200:
            return AccountErrors.SocialLoginFailed(accept_status, social_provider=social_provider_translation.get(social_user.provider))
        try:
            accept_json = accept.json()
        except requests.exceptions.JSONDecodeError:
            accept_json = json.load(accept)
        print(accept_json)

        res = JsonResponse(accept_json, status=200)
        return res
    # Signup Request
    except User.DoesNotExist:
        # 기존에 가입된 유저가 없으면 등록된 회원이 없으니 바로 회원가입 진행
        data = {'access_token': access_token, 'code': code}
        print(data)
        # TODO 이거 바꾸기 (local : 127.0.0.1:8000)
        accept = requests.post(f"http://0.0.0.0:8000/api/user/google/login/finish", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return AccountErrors.SocialLoginFailed(email_req_status, social_provider="구글")
        accept_json = accept.json()
        print(accept_json)
        user = accept_json.get('user')
        user_instance = get_object_or_404(User, id=user['pk'])
        with transaction.atomic():
            user_instance.save()
            Table.objects.create(user_id=user["pk"], main=True)
        accept_json['user'] = user

        res = JsonResponse(accept_json, status=201)
        return res
    except SocialAccount.DoesNotExist:
        res = AccountErrors.UserAlreadyExist(400, email, social_provider="이메일")
        return res


class GoogleLogin(SocialLoginView):
    adapter_class = google_view.GoogleOAuth2Adapter
    callback_url = GOOGLE_CALLBACK_URI
    client_class = OAuth2Client
    
    def get_response_serializer(self):
        if getattr(settings, 'REST_USE_JWT', False):
            response_serializer = JWTCustomSerializer

        else:
            response_serializer = TokenSerializer
        return response_serializer
    
    def get_response(self):
        serializer_class = self.get_response_serializer()

        if getattr(settings, 'REST_USE_JWT', False):
            from rest_framework_simplejwt.settings import (
                api_settings as jwt_settings,
            )
            access_token_expiration = (timezone.now() + jwt_settings.ACCESS_TOKEN_LIFETIME)
            refresh_token_expiration = (timezone.now() + jwt_settings.REFRESH_TOKEN_LIFETIME)
            return_expiration_times = getattr(settings, 'JWT_AUTH_RETURN_EXPIRATION', False)
            auth_httponly = getattr(settings, 'JWT_AUTH_HTTPONLY', False)

            data = {
                'user': self.user,
                'access': self.access_token,
            }

            if not auth_httponly:
                data['refresh'] = self.refresh_token
            else:
                # Wasnt sure if the serializer needed this
                data['refresh'] = ""

            if return_expiration_times:
                data['access_token_expiration'] = access_token_expiration
                data['refresh_token_expiration'] = refresh_token_expiration

            serializer = serializer_class(
                instance=data,
                context=self.get_serializer_context(),
            )
        elif self.token:
            serializer = serializer_class(
                instance=self.token,
                context=self.get_serializer_context(),
            )
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)
        response = Response(serializer.data, status=status.HTTP_200_OK)
        if getattr(settings, 'REST_USE_JWT', False):
            set_jwt_cookies(response, self.access_token, self.refresh_token)
        print(response.cookies.get("access"))

        return response
    

class UserViewSets(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'user_id'
    
    def update(self, request, user_id, *args, **kwargs):
        partial = True
        if request.user.id != user_id:
            return Response(status=status.HTTP_403_FORBIDDEN, data={"message": "자신의 정보만 변경할 수 있습니다."})
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
