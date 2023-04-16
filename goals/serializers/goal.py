from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.serializers import UserSerializer
from goals.models.board import BoardParticipant
from goals.models.goal import Goal


class GoalListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = "__all__"
        read_only_fields = ("__all__",)


class GoalCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Goal
        fields = "__all__"
        read_only_fields = ("id", "created", "user", "updated")

    def validate(self, attrs: dict) -> dict:
        role_use = BoardParticipant.objects.filter(
            user=attrs.get('user'),
            board=attrs.get('category').board,
            role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer]
        )

        if not role_use:
            raise ValidationError('Недостаточно прав')

        return attrs


class GoalSerializer(serializers.ModelSerializer):
    """Данный сериалайзер потребовался для того, чтобы убрать
    логику с подстановкой текущего пользователя в поле user."""
    user = UserSerializer(read_only=True)

    class Meta:
        model = Goal
        fields = "__all__"
        read_only_fields = ("id", "created", "user", "updated")
