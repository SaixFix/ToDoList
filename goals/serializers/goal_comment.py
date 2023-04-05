from rest_framework import serializers

from core.serializers import UserSerializer
from goals.models.goal import Goal
from goals.models.goal_comment import GoalComment


class GoalCommentCreateSerializer(serializers.ModelSerializer):
    #  при создании категории в поле user будет проставлен
    #  тот пользователь, от чьего имени создавалась категория.
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalComment
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")

    def validate_goal(self, value):
        # проверка на владельца
        if value.user != self.context["request"].user:
            raise serializers.ValidationError("not owner of goal")

        return value


class GoalCommentSerializer(serializers.ModelSerializer):
    """Этот сериалайзер потребовался для того, чтобы убрать
        логику с подстановкой текущего пользователя в поле user."""
    user = UserSerializer(read_only=True)

    class Meta:
        model = GoalComment
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user", "goal")

    def validate_goal(self, value):
        if value.status == Goal.status == 4:
            raise serializers.ValidationError('Goal not found')
        # проверка на владельца
        if value.user != self.context["request"].user:
            raise serializers.ValidationError("not owner of goal")
