from typing import Callable
from unittest.mock import ANY

from rest_framework import status
import pytest
from django.urls import reverse
import factory.django


@pytest.fixture()
def user_create_data(faker) -> Callable:
    def _wrapper(**kwargs) -> dict:
        password = faker.password(8)
        data = {
            'username': faker.user_name(),
            'password': password,
            'password_repeat': password
        }
        data |= kwargs
        return data

    return _wrapper


@pytest.mark.django_db()
class TestUserSignup:
    url = reverse('create_user')

    def test_signup_user(self, client, user_create_data):
        """
        Тест на регистрацию юзера
        """
        data = user_create_data()
        response = client.post(self.url, data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == self._serialize_user_response(
            username=data['username']
        )

    def test_passwords_match(self, client, user_create_data):
        """
        При разных значениях в полях: пароль и повтор пароля 400
        """
        data = user_create_data(
            password_repeat=factory.Faker('password', length=8)
        )
        response = client.post(self.url, data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def _serialize_user_response(self, **kwargs) -> dict:
        data = {
            'username': ANY,
            'first_name': '',
            'last_name': '',
            'email': '',
            'password': ANY
        }
        data |= kwargs
        return data
