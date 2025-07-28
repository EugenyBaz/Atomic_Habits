from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from users.views import RegistrationView

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/',
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name='login'),
]