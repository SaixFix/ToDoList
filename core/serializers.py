from rest_framework import serializers

from core.models import User
from core.validators import check_password_validate_and_match


class UserCreateSerializer(serializers.ModelSerializer):
    password_repeat = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'password_repeat')

    def create(self, validated_data: dict) -> User:
        password = self.initial_data.pop('password')
        password_repeat = self.initial_data.pop('password_repeat')

        # проверка на совпадение паролей
        check_password_validate_and_match(password, password_repeat)

        del validated_data['password_repeat']

        user = User.objects.create(**validated_data)

        # хешируем пароль
        user.set_password(user.password)
        user.save()
        return user


class UserRetrieveUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
