import django_filters
from django.db import models
from django_filters import rest_framework

from goals.models.goal import Goal
from goals.models.goal_comment import GoalComment


class GoalDateFilter(rest_framework.FilterSet):
    class Meta:
        model = Goal
        # поля и разрешенные lookup (поиски) по ним.
        fields = {
            "due_date": ("lte", "gte"),
            "category": ("exact", "in"),
            "status": ("exact", "in"),
            "priority": ("exact", "in"),
        }

    # реализация фильтра для DateTimeField
    filter_overrides = {
        models.DateTimeField: {"filter_class": django_filters.IsoDateTimeFilter},
    }


class GoalCommentDateFilter(rest_framework.FilterSet):
    class Meta:
        model = GoalComment
        # поля и разрешенные lookup (поиски) по ним.
        fields = {
            "goal": ("exact",),
        }
