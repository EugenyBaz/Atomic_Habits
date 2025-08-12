from datetime import datetime
from unittest.mock import patch

import requests
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from config import settings
from habits.models import Habit
from habits.services import send_telegram_message
from users.models import User


class HabitTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@example.ru")

        parsed_time = datetime.strptime("19:00:00", "%H:%M:%S").time()

        # Создаём привычку минимально необходимым набором данных
        self.habit = Habit.objects.create(
            user=self.user,
            place="любое",
            time=parsed_time,
            action="Позвонить родителям",
            pleasant_habit=True,
            periodicity_days=7,
            execution_time=60,
            public=True,
            owner=self.user,  # Явно указываем владельца
        )

        # Авторизуем клиента под этим пользователем
        self.client.force_authenticate(user=self.user)

    def test_create_habit(self):
        # Формируем URL для создания привычки
        url = reverse("habits:habit-list")  # Проверь корректность паттерна URL

        # Данные для создания новой привычки
        data = {
            "user": self.user.pk,
            "place": "любое",
            "time": "00:55:00",
            "action": "Сделать подход на пресс",
            "pleasant_habit": True,
            "periodicity_days": 7,
            "reward": "",
            "execution_time": 60,
            "public": True,
        }

        # Отправляем POST-запрос на создание привычки
        response = self.client.post(url, data, format="json")

        # Проверяем статус ответа
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Проверяем, что привычка создана
        new_habit = Habit.objects.latest("id")
        self.assertEqual(new_habit.place, data["place"])
        self.assertEqual(new_habit.action, data["action"])

    def test_habbit_list(self):
        url = reverse("habits:habit-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_habit_update(self):
        url = reverse("habits:habit-detail", args=(self.habit.pk,))
        data = {"action": "Любое действие"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("action"), "Любое действие")

    def test_habit_delete(self):
        url = reverse("habits:habit-detail", args=(self.habit.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.all().count(), 0)

    @patch("habits.services.requests.get")  # Патчмим модуль requests.get
    def test_successful_send(self, mock_get):
        """Тестируем успешную отправку сообщения"""
        chat_id = "123"
        message = "Test Message"

        # Настройка моков
        mock_response = mock_get.return_value
        mock_response.status_code = 200  # Устанавливаем успешный статус
        mock_response.ok = True
        mock_response.raise_for_status.side_effect = None  # Нет ошибок

        # Выполняем нашу функцию
        send_telegram_message(chat_id, message)

        # Проверяем правильность вызова запроса
        expected_url = (
            f"{settings.TELEGRAM_URL}{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
        )
        mock_get.assert_called_once_with(
            expected_url, params={"text": message, "chat_id": chat_id}
        )

    @patch("habits.services.requests.get")
    def test_failed_send(self, mock_get):
        """Тестируем случай, когда произошла ошибка при отправке сообщения."""
        chat_id = "123"
        message = "Test Message"

        # Настройка моков
        mock_response = mock_get.return_value
        mock_response.status_code = 400  # Ошибка (Bad Request)
        mock_response.ok = False
        mock_response.text = "Ошибка при отправке сообщения."
        mock_response.raise_for_status.side_effect = lambda: requests.HTTPError(
            response=mock_response
        )

        result = send_telegram_message(chat_id, message)

        expected_url = (
            f"{settings.TELEGRAM_URL}{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
        )
        mock_get.assert_called_once_with(
            expected_url, params={"text": message, "chat_id": chat_id}
        )

        assert not result, "Ожидалась ошибка отправки сообщения"
