from base64 import urlsafe_b64decode, urlsafe_b64encode
from django.core.mail import EmailMessage
from tokenize import TokenError
from django.utils.encoding import force_str, force_bytes
from django.shortcuts import redirect

import jwt

from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from accountapp.text import message

from config.settings import SECRET_KEY
from accountapp.models import User
from accountapp.serializers import MyTokenObtainPairSerializer, RegisterSerializer
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework import status

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
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)
            return res
        except TokenError as e:
            raise jwt.InvalidTokenError(e.args[0])


def send_verification_email(title="이메일 인증을 완료해주세요", data=None, to=None):
    mail_title      = "이메일 인증을 완료해주세요"
    mail_to         = to
    email           = EmailMessage(
        mail_title, 
        data, 
        to = [mail_to])
    print(email.send())
    return

# 회원가입
class RegisterAPIView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            if not serializer.check_password(validated_data=serializer.validated_data):
                return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "Passwords don't match"})
            
            user = serializer.save()
            
            current_site    = Site.objects.get_current()
            domain          = current_site.domain
            print(user.pk)
            # uidb64          = urlsafe_b64encode(bytes(str(user.pk), 'UTF-8')).encode('UTF-8')
            uidb64          = user.id

            token           = jwt.encode({'user':user.id}, SECRET_KEY, algorithm='HS256')
            message_data    = message(domain, uidb64, token)
            mail_title      = "이메일 인증을 완료해주세요"
            
            send_verification_email(mail_title, message_data, request.data["email"])
            
            return Response({"message": "register successs. Please"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Activate(APIView):
    def get(self, request, uidb64, token):
        try:
            uid = uidb64
            print(uid)
            user = User.objects.get(id=uid)
            print(user)
            user_dic = jwt.decode(token, SECRET_KEY, algorithms='HS256')
            print(user_dic)
            if user.id == user_dic["user"]:
                user.is_active = True
                user.save()
                # res = Response(
                #     {
                #         "user": user,
                #         "message": "email_verify successs"
                #     },
                #     status=status.HTTP_200_OK,
                # )
                return redirect("http://127.0.0.1:8000/api/user/login")

            return Response({'message':'auth fail'}, status=400)
        except ValidationError:
            return Response({'message':'type_error'}, status=400)
        except KeyError:
            return Response({'message':'INVALID_KEY'}, status=400)