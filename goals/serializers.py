from rest_framework import serializers

from core.serializers import UserCreateSerializer
from goals.models import GoalCategory


class GoalCreateSerializer(serializers.ModelSerializer):
    #  при создании категории в поле user будет проставлен
    #  тот пользователь, от чьего имени создавалась категория.
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalCategory
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"


class GoalCategorySerializer(serializers.ModelSerializer):
    """Новый сериалайзер потребовался для того, чтобы убрать
    логику с подстановкой текущего пользователя в поле user."""
    user = UserCreateSerializer(read_only=True)

    class Meta:
        model = GoalCategory
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")
