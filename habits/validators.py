from django.core.validators import BaseValidator
from django.core.validators import ValidationError


class ExecutionTimeValidator(BaseValidator):

    """ Проверяет что бы время выполнения было  не больше 120 секунд."""

    message = "Время выполнения привычки не должно превышать %(limit_value)s секунд."

    def compare(self, value, limit_value):
        return value > limit_value

class PeriodicityValidator(BaseValidator):

    """ Проверяет чтобы привычка выполнялась не реже, чем 1 раз в 7 дней. """
    message = "Периодичность должна быть от 1 до 7 дней."

    def compare(self, value, limit_value):
        return not (1 <= value <= limit_value)

class RelatedAndRewardValidator(object):

    """ Исключает одновременный выбор связанной привычки и указания вознаграждения."""

    def __call__(self, habit):
        if habit.related_habit and habit.rewards:
            raise ValidationError("Нельзя одновременно указывать связанную привычку и награду.")

        if habit.related_habit and not habit.related_habit.pleasant_habit:
            raise ValidationError("Связанной может быть только приятная привычка.")

        if habit.pleasant_habit and (habit.related_habit or habit.rewards):
            raise ValidationError("Приятная привычка не может иметь связанную привычку или награду.")