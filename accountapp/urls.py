from django.urls import path
from accountapp.views import Activate, MyTokenObtainPairView, RegisterAPIView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'accountapp'

urlpatterns = [
    # Django Rest Auth
    path('login', MyTokenObtainPairView.as_view(), name='login'),
    path('token/refresh', TokenRefreshView.as_view(), name='refresh'),
    path('registration', RegisterAPIView.as_view(), name='register'),
    
    path('activate/<int:uidb64>/<str:token>', Activate.as_view())
]
