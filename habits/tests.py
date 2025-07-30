from datetime import datetime

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
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
            owner=self.user  # Явно указываем владельца
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
            "public": True
        }

        # Отправляем POST-запрос на создание привычки
        response = self.client.post(url, data, format='json')

        # Проверяем статус ответа
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Проверяем, что привычка создана
        new_habit = Habit.objects.latest('id')
        self.assertEqual(new_habit.place, data['place'])
        self.assertEqual(new_habit.action, data['action'])

    # def test_lesson_retrieve(self):
    #     url = reverse("lms:lesson_retrieve", args=(self.lesson.pk,))
    #     response = self.client.get(url)
    #     data = response.json()
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(data.get("name"), self.lesson.name)
    #

    #
    # def test_lesson_update(self):
    #     url = reverse("lms:lesson_update", args=(self.lesson.pk,))
    #     data = {"name": "Урок тестовый"}
    #     response = self.client.patch(url, data)
    #     data = response.json()
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(data.get("name"), "Урок тестовый")
    #
    # def test_lesson_delete(self):
    #     url = reverse("lms:lesson_delete", args=(self.lesson.pk,))
    #     response = self.client.delete(url)
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    #     self.assertEqual(Lesson.objects.all().count(), 0)
    #
    # def test_lesson_list(self):
    #     url = reverse("lms:lesson_list")
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #
    # def test_subscribe_course(self):
    #     url = reverse("lms:subscribe-unsubscribe")
    #     data = {
    #         "course_id": self.course.id,
    #     }
    #     response = self.client.post(url, data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data["message"], "Подписка добавлена.")
    #     self.assertTrue(
    #         Subscription.objects.filter(user=self.user, course=self.course).exists()
    #     )
