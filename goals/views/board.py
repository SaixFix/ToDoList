from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from goals.models.board import Board
from goals.models.goal import Goal
from goals.permissions import BoardPermissions
from goals.serializers.board import BoardCreateSerializer, BoardSerializer


class BoardCreateView(generics.CreateAPIView):
    model = Board
    serializer_class = BoardCreateSerializer
    permission_classes = [IsAuthenticated]


class BoardListView(generics.ListAPIView):
    model = Board
    serializer_class = BoardCreateSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = LimitOffsetPagination
    filter_backends = [
        DjangoFilterBackend,  # подключение бэкэнд фильтрации
        OrderingFilter,  # упорядочить
    ]
    ordering_fields = ['title']

    def get_queryset(self):
        return Board.objects.filter(
            participants__user_id=self.request.user.id,
            is_deleted=False
        )


class BoardView(RetrieveUpdateDestroyAPIView):
    model = Board
    permission_classes = [BoardPermissions]
    serializer_class = BoardSerializer

    def get_queryset(self):
        # Фильтрация идет через participants
        return Board.objects.filter(is_deleted=False)

    def perform_destroy(self, instance):
        # При удалении доски помечаем ее как is_deleted,
        # «удаляем» категории, обновляем статус целей
        with transaction.atomic():
            instance.is_deleted = True
            instance.save()
            instance.categories.update(is_deleted=True)
            Goal.objects.filter(category__board=instance).update(
                status=Goal.status == 4
            )
        return instance
