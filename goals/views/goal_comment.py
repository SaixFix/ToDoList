from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination

from goals.filters import GoalCommentDateFilter
from goals.models.goal_comment import GoalComment
from goals.permissions import GoalCommentPermissions
from goals.serializers.goal_comment import GoalCommentSerializer, GoalCommentCreateSerializer


class GoalCommentCreateView(generics.CreateAPIView):
    model = GoalComment
    serializer_class = GoalCommentCreateSerializer
    permission_classes = [GoalCommentPermissions]


class GoalCommentListView(generics.ListAPIView):
    model = GoalComment
    serializer_class = GoalCommentSerializer
    permission_classes = [GoalCommentPermissions]
    pagination_class = LimitOffsetPagination
    filter_backends = [
        DjangoFilterBackend,  # подключение бэкэнд фильтрации
        OrderingFilter,  # упорядочить
    ]
    ordering_fields = ['created']
    filterset_class = GoalCommentDateFilter

    def get_queryset(self):
        return GoalComment.objects.filter(goal__category__board__participants__user_id=self.request.user.id).order_by('-created')


class GoalCommentView(RetrieveUpdateDestroyAPIView):
    model = GoalComment
    serializer_class = GoalCommentSerializer
    permission_classes = [GoalCommentPermissions]

    def get_queryset(self):
        return GoalComment.objects.select_related('user').filter(user=self.request.user)
