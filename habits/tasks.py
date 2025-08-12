from datetime import time
from celery import shared_task
from django.utils import timezone
from django.utils.timezone import localtime
from django_celery_beat.schedulers import logger
from habits.models import Habit
from habits.services import send_telegram_message


@shared_task
def send_message_start_actions():
    """Отправляет сообщение в установленное время о начале выполнения привычки"""

    current_local_time = localtime(timezone.now()).time()

    formatted_time = time(current_local_time.hour, current_local_time.minute)
    print(f"Отформатированное  время: {formatted_time}")

    habits = Habit.objects.filter(owner__isnull=False, time=formatted_time)

    for habit in habits:
        if habit.owner.tg_chat_id:
            print(habit.owner.tg_chat_id)
            try:
                message = f"Пора {habit.action.lower()}!"
                send_telegram_message(habit.owner.tg_chat_id, message)
                logger.info(
                    f"Сообщение успешно отправлено пользователю {habit.owner.email}."
                )
            except Exception as e:
                logger.error(
                    f"Ошибка отправки сообщения пользователю {habit.owner.email}: {e}"
                )

    return f"Отправлено такое количество привычек: {len(habits)}"
