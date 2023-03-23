from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, AuthenticationFailed

from core.models import User


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True)
    password_repeat = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'password_repeat')

    def validate(self, attrs: dict) -> dict:
        """Проверяем пароли на совпадение и прогоняем по валидаторам"""

        validate_password(attrs['password'])

        if attrs['password'] != attrs['password_repeat']:
            raise ValidationError(
                {'check_password_match': 'пароли не совпадают'}
            )
        return attrs

    def create(self, validated_data: dict) -> User:
        del validated_data['password_repeat']

        # хешируем пароль и сохраняет пользователя 1 запросом к базе
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class UserRetrieveUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'password')

    def create(self, validated_data):
        user = authenticate(
            username=validated_data['username'],
            password=validated_data['password']
        )

        if not user:
            raise AuthenticationFailed
        return user
