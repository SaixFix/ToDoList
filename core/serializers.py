from rest_framework import serializers

from core.models import User


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):

        user = User.objects.create(**validated_data)

        # хешируем пароль
        user.set_password(user.password)
        user.save()
        return user
