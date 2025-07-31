from django.urls import include, path
from rest_framework.routers import DefaultRouter

from habits.views import HabitViewSet, PublicHabitViewSet

router = DefaultRouter()

router.register(r"habit", HabitViewSet, basename="habit")
router.register(r"public", PublicHabitViewSet, basename="public")

app_name = "habits"

urlpatterns = [
    path("", include(router.urls)),
]
