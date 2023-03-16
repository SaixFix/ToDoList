from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.models import User


def check_password_match(password: str, password_repeat: str):
    if password_repeat != password:
        raise ValidationError(
            'пароли не совпадают'
        )
