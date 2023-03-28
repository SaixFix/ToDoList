from rest_framework import serializers

from core.serializers import UserSerializer
from goals.models import GoalCategory, Goal


class GoalCategoryCreateSerializer(serializers.ModelSerializer):
    #  при создании категории в поле user будет проставлен
    #  тот пользователь, от чьего имени создавалась категория.
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalCategory
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")


class GoalCategorySerializer(serializers.ModelSerializer):
    """Новый сериалайзер потребовался для того, чтобы убрать
    логику с подстановкой текущего пользователя в поле user."""
    user = UserSerializer(read_only=True)

    class Meta:
        model = GoalCategory
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")


class GoalCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Goal
        fields = "__all__"
        read_only_fields = ("id", "created", "user")

    def validate_category(self, value):
        if value.is_deleted:
            raise serializers.ValidationError("not allowed in deleted category")

        if value.user != self.context["request"].user:
            raise serializers.ValidationError("not owner of category")

        return value
