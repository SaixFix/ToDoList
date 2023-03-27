from django.shortcuts import render
from rest_framework import permissions, filters
from rest_framework import generics

from goals.models import GoalCategory
from goals.serializers import GoalCreateSerializer, GoalCategorySerializer


class GoalCategoryCreateView(generics.CreateAPIView):
    model = GoalCategory
    serializer_class = GoalCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


class GoalCategoryListView(generics.ListAPIView):
    model = GoalCategory
    serializer_class = GoalCategorySerializer
    filter_backends = [
        filters.OrderingFilter,  # фильтр сортировки
        filters.SearchFilter,   # фильтр поиска по вхождению
    ]
    ordering_fields = ["title", "created"]
    ordering = ["title"]  # сортировка по умолчанию
    search_fields = ["title"]

    def get_queryset(self):
        """Фильтруем по пользователю и только со статусом не удаленная"""
        return GoalCategory.objects.filter(
            user=self.request.user, is_deleted=False
        )
