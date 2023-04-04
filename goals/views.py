from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, filters
from rest_framework import generics
from rest_framework.generics import RetrieveUpdateDestroyAPIView

from goals.filters import GoalDateFilter
from goals.models import GoalCategory, Goal
from goals.serializers import GoalCategorySerializer, GoalCategoryCreateSerializer, GoalListSerializer, \
    GoalCreateSerializer, GoalSerializer


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

    def perform_destroy(self, instance: GoalCategory):
        """переназначаем  функцию чтобы категории не удалялись при вызове delete,
         меняем статус у всех связанных с категорией целях,
         меняем значение is_deleted"""
        instance.goals.update(status=4)
        instance.is_deleted = True
        instance.save()
        return instance


class GoalListView(generics.ListAPIView):
    model = Goal
    serializer_class = GoalListSerializer
    filter_backends = [
        DjangoFilterBackend,
    ]
    filterset_class = GoalDateFilter

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)


class GoalCreateView(generics.CreateAPIView):
    model = Goal
    serializer_class = GoalCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


class GoalView(RetrieveUpdateDestroyAPIView):
    model = Goal
    serializer_class = GoalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)

    def perform_destroy(self, instance: Goal):
        """переназначаем  функцию чтобы цель не удалялись при вызове delete,
         меняем значение status"""
        instance.status = 4
        instance.save()
        return instance

