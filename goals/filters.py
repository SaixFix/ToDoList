import django_filters
from django.db import models
from django_filters import rest_framework

from goals.models import Goal


class GoalDateFilter(rest_framework.FilterSet):
    class Meta:
        model = Goal
        # поля и разрешенные lookup (поиски) по ним.
        fields = {
            "deadline_date": ("lte", "gte"),
            "category": ("exact", "in"),
            "status": ("exact", "in"),
            "priority": ("exact", "in"),
        }

    # реализация фильтра для DateTimeField
    filter_overrides = {
        models.DateTimeField: {"filter_class": django_filters.IsoDateTimeFilter},
    }
