from datetime import time, timedelta

from celery import shared_task
from django.utils import timezone
from django.utils.timezone import now

from habits.models import Habit
from habits.services import send_telegram_message
from users.models import User


@shared_task
def send_message_start_actions():
    """Отправляет сообщение в установленное время о начале выполнения привычки"""

    current_time = timezone.now()

    habits = Habit.objects.filter(owner__isnull=False, time=current_time)

    for habit in habits:
        if habit.owner.tg_chat_id:
            try:
                message = f"Пора {habit.action.lower()}!"
                send_telegram_message(habit.owner.tg_chat_id, message)
            except Exception as e:
                print(f'Ошибка отправки сообщения: {e}')

