from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from habits.models import Habit
from habits.pagination import MyPagination
from habits.serializers import HabitSerializer, PublicHabitSerializer


class HabitViewSet(ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    pagination_class = MyPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Получаем привычки только текущего пользователя
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        habit = serializer.save()
        habit.owner = self.request.user
        habit.save()


class PublicHabitViewSet(ModelViewSet):
    queryset = Habit.objects.filter(public=True)
    serializer_class = PublicHabitSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = MyPagination
    http_method_names = ["get"]
