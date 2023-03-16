from rest_framework import serializers

from core.models import User
from core.validators import check_password_match


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        password = self.initial_data.pop('password')
        password_repeat = self.initial_data.pop('password_repeat')

        # проверрка на совпадение паролей
        check_password_match(password, password_repeat)

        user = User.objects.create(**validated_data)

        # хешируем пароль
        user.set_password(user.password)
        user.save()
        return user
