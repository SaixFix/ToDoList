from django.db import models

from core.models import User
from goals.models.base_mixin import DatesModelMixin
from goals.models.goal_category import GoalCategory


class Status(models.IntegerChoices):
    to_do = 1, "К выполнению"
    in_progress = 2, "В процессе"
    done = 3, "Выполнено"
    archived = 4, "Архив"


class Priority(models.IntegerChoices):
    low = 1, "Низкий"
    medium = 2, "Средний"
    high = 3, "Высокий"
    critical = 4, "Критический"


class Goal(DatesModelMixin):
    class Meta:
        verbose_name = "Цель"
        verbose_name_plural = "Цели"

    title = models.CharField(verbose_name="Название", max_length=200)
    description = models.CharField(verbose_name="Описание", max_length=500)
    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.CASCADE)
    category = models.ForeignKey(
        GoalCategory, verbose_name="Категория",
        on_delete=models.PROTECT, related_name="goals"
    )
    due_date = models.DateTimeField(verbose_name="Дата дедлайна", null=True, blank=True)
    status = models.PositiveSmallIntegerField(
        verbose_name="Статус", choices=Status.choices, default=Status.to_do
    )
    priority = models.PositiveSmallIntegerField(
        verbose_name="Приоритет", choices=Priority.choices, default=Priority.medium
    )

    def __str__(self):
        return self.title
