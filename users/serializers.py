from rest_framework import serializers

from habits.models import Habit
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {"password": {"write_only": True}}


class PublicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email']

class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = ['action', 'place', 'time']