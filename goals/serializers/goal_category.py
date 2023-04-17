from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.serializers import UserSerializer
from goals.models.board import BoardParticipant
from goals.models.goal_category import GoalCategory


class GoalCategoryCreateSerializer(serializers.ModelSerializer):
    #  при создании категории в поле user будет проставлен
    #  тот пользователь, от чьего имени создавалась категория.
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalCategory
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user", "is_deleted")

    def validate(self, attrs: dict) -> dict:
        role_user = BoardParticipant.objects.filter(
            user=attrs.get('user'),
            board=attrs.get('board'),
            role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer]
        ).exists()

        if not role_user:
            raise ValidationError('Недостаточно прав')

        return attrs


class GoalCategorySerializer(serializers.ModelSerializer):
    """Этот сериалайзер потребовался для того, чтобы убрать
    логику с подстановкой текущего пользователя в поле user."""
    user = UserSerializer(read_only=True)

    class Meta:
        model = GoalCategory
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")