from django.urls import path
from accountapp.views import Activate, EmailResend, GoogleLogin, MyTokenObtainPairView, RegisterAPIView, UserViewSets, google_login

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'accountapp'

urlpatterns = [
    # Django Rest Auth
    path('/login', MyTokenObtainPairView.as_view(), name='login'),
    path('/token/refresh', TokenRefreshView.as_view(), name='refresh'),
    path('/registration', RegisterAPIView.as_view(), name='register'),
    path('/<int:id>', UserViewSets.as_view({'put': 'update'})),
    path('/email/resend', EmailResend.as_view()),
    
    path('/activate/<int:uidb64>/<str:token>', Activate.as_view()),
    # path('/google/redirect', google_redirect, name='google_redirect'),
    path('/google/login', google_login, name='google_login'),
    path('/google/login/finish', GoogleLogin.as_view(), name='google_login_finish')
]
