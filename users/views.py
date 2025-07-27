from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from habits.models import Habit
from users.models import User
from users.serializers import UserSerializer, PublicUserSerializer, HabitSerializer


class UserViewSet(ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        if obj != self.request.user:
            raise PermissionDenied("Нельзя смотреть чужой профиль")
        return obj

    def get_serializer_class(self):
        if self.action == 'list':
            return PublicUserSerializer
        return UserSerializer

class PublicHabitViewSet(ModelViewSet):
    queryset = Habit.objects.filter(public=True)
    serializer_class = HabitSerializer
    http_method_names = ['get']