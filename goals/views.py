from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, filters
from rest_framework import generics
from rest_framework.generics import RetrieveUpdateDestroyAPIView

from goals.filters import GoalDateFilter
from goals.models import GoalCategory, Goal
from goals.serializers import GoalCreateSerializer, GoalCategorySerializer, GoalCategoryCreateSerializer


class GoalCategoryCreateView(generics.CreateAPIView):
    model = GoalCategory
    serializer_class = GoalCategoryCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


class GoalCategoryListView(generics.ListAPIView):
    model = GoalCategory
    serializer_class = GoalCategorySerializer
    filter_backends = [
        filters.OrderingFilter,  # фильтр сортировки
        filters.SearchFilter,  # фильтр поиска по вхождению
    ]
    ordering_fields = ["title", "created"]
    ordering = ["title"]  # сортировка по умолчанию
    search_fields = ["title"]

    def get_queryset(self):
        """Фильтруем по пользователю и только со статусом не удаленная"""
        return GoalCategory.objects.filter(
            user=self.request.user, is_deleted=False
        )


class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    model = GoalCategory
    serializer_class = GoalCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return GoalCategory.objects.filter(user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance):
        """чтобы категории не удалялись при вызове delete"""
        instance.is_deleted = True
        instance.save()
        return instance


class GoalListView(generics.ListAPIView):
    model = Goal
    filter_backends = [
        DjangoFilterBackend,
    ]
    filterset_class = GoalDateFilter
