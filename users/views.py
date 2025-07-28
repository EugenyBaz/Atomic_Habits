from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet

from habits.models import Habit
from users.models import User
from users.serializers import UserSerializer, PublicUserSerializer, RegisterSerializer


class RegistrationView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        data = serializer.validated_data
        password = data.pop("password")
        user = serializer.save(is_active=True)
        user.set_password(password)
        user.save()


class UserViewSet(ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return PublicUserSerializer
        return UserSerializer

