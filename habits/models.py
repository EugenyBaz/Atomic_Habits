from django.db import models

from habits.validators import ExecutionTimeValidator, PeriodicityValidator, RelatedAndRewardValidator
from users.models import User


class Habit(models.Model):
        #Пользователь — создатель привычки.
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
        # Место — место, в котором необходимо выполнять привычку.
    place = models.CharField(max_length=300, verbose_name="Место")
        # Время — время, когда необходимо выполнять привычку.
    time = models.TimeField(verbose_name="Время назначенное для выполнения")
        # Действие — действие, которое представляет собой привычка.
    action = models.CharField(max_length=500, verbose_name="Действие")
        # Признак приятной привычки — привычка, которую можно привязать к выполнению полезной привычки.
    pleasant_habit = models.BooleanField(default=False, verbose_name="Признак приятной привычки")
        # Связанная привычка — привычка, которая связана с другой привычкой, важно указывать для полезных привычек, но не для приятных.
    related_habit = models.ForeignKey("self",null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Связанная привычка")
        # Периодичность (по умолчанию ежедневная) — периодичность выполнения привычки для напоминания в днях.
    periodicity_days = models.PositiveIntegerField(validators=[PeriodicityValidator(limit_value=7)], default=1, verbose_name="Периодичность")
        # Вознаграждение — чем пользователь должен себя вознаградить после выполнения.
    reward = models.CharField(max_length=300, blank=True, verbose_name="Вознаграждение")
        # Время на выполнение — время, которое предположительно потратит пользователь на выполнение привычки.
    execution_time = models.PositiveSmallIntegerField(validators=[
        ExecutionTimeValidator(120)], verbose_name="Время на выполнение")
        # Признак публичности — привычки можно публиковать в общий доступ, чтобы другие пользователи могли брать в пример чужие привычки.
    public = models.BooleanField(default=False, verbose_name="Признак публичности")

    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Владелец привычки", related_name='owned_habits')

    def clean(self):
        super().clean()  # Запускает автоматические валидаторы для всех полей
        validator = RelatedAndRewardValidator()
        validator(self)

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"

    def __str__(self):
        return f"{self.user.username}'s habit: {self.action}"