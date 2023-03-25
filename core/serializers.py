from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password, check_password
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
        fields = ('id', 'first_name', 'last_name', 'username', 'email')
        read_only_fields = ('id',)


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email', 'password')
        read_only_fields = ('id', 'first_name', 'last_name', 'username', 'email')

    def create(self, validated_data):
        user = authenticate(
            username=validated_data['username'],
            password=validated_data['password']
        )

        if not user:
            raise AuthenticationFailed
        return user


class PasswordChangeSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True, required=True, min_length=1)
    new_password = serializers.CharField(write_only=True, required=True, min_length=1)

    class Meta:
        model = User
        fields = ('new_password', 'old_password')

    def update(self, instance: User, validated_data: dict) -> User:
        old_password = validated_data['old_password']
        new_password = validated_data['new_password']
        if not instance.check_password(old_password):
            raise ValidationError('old_password не верен')

        validate_password(new_password)

        instance.set_password(new_password)
        instance.save()

        return instance


