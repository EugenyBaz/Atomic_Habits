from django.contrib import admin

from habits.models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display= (
        "id",
        "user",
        "place",
        "time",
        "action",
        "pleasant_habit",
        "related_habit",
        "periodicity_days",
        "reward",
        "execution_time",
        "public",
    )
    ordering = ("id",)

