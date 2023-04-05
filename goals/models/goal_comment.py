from django.db import models
from django.utils import timezone

from core.models import User
from goals.models.base_mixin import DatesModelMixin
from goals.models.goal import Goal


class GoalComment(DatesModelMixin):
    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    goal = models.ForeignKey(Goal, verbose_name="Цель", on_delete=models.CASCADE)

    def __str__(self):
        return self.text
