from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions
from rest_framework.generics import RetrieveUpdateDestroyAPIView

from goals.filters import GoalDateFilter
from goals.models.goal import Goal
from goals.serializers.goal import GoalListSerializer, GoalCreateSerializer, GoalSerializer


class GoalListView(generics.ListAPIView):
    model = Goal
    serializer_class = GoalListSerializer
    filter_backends = [
        DjangoFilterBackend,  # подключение бэкэнд фильтрации
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
