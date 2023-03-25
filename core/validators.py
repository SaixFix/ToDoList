from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.models import User

#TODO удалить
def check_password_validate_and_match(password: str, password_repeat: str):

    validate_password(password)

    if password_repeat != password:
        raise ValidationError(
            'пароли не совпадают'
        )

