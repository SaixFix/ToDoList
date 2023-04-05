from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions
from rest_framework.filters import OrderingFilter
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination

from goals.filters import GoalCommentDateFilter
from goals.models.goal_comment import GoalComment
from goals.serializers.goal_comment import GoalCommentSerializer, GoalCommentCreateSerializer


class GoalCommentCreateView(generics.CreateAPIView):
    model = GoalComment
    serializer_class = GoalCommentCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


class GoalCommentListView(generics.ListAPIView):
    model = GoalComment
    serializer_class = GoalCommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = LimitOffsetPagination
    filter_backends = [
        DjangoFilterBackend,  # подключение бэкэнд фильтрации
        OrderingFilter,  # упорядочить
    ]
    ordering_fields = ['created']
    filterset_class = GoalCommentDateFilter

    def get_queryset(self):
        return GoalComment.objects.filter(user=self.request.user).order_by('-created')


class GoalCommentView(RetrieveUpdateDestroyAPIView):
    model = GoalComment
    serializer_class = GoalCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return GoalComment.objects.filter(user=self.request.user)
