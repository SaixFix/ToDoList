from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination

from goals.filters import GoalDateFilter
from goals.models.goal import Goal
from goals.permissions import GoalPermissions
from goals.serializers.goal import GoalListSerializer, GoalCreateSerializer, GoalSerializer


class GoalCreateView(generics.CreateAPIView):
    model = Goal
    serializer_class = GoalCreateSerializer
    permission_classes = [GoalPermissions]


class GoalListView(generics.ListAPIView):
    model = Goal
    serializer_class = GoalListSerializer
    permission_classes = [GoalPermissions]
    filter_backends = [
        DjangoFilterBackend,  # подключение бэкэнд фильтрации
    ]
    filterset_class = GoalDateFilter
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return Goal.objects.filter(category__board__participants__user=self.request.user)


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
