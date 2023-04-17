import pytest
from rest_framework.test import APIClient

from core.models import User

pytest_plugins = 'tests.factories'


@pytest.fixture()
def client() -> APIClient:
    """Вернет неавторизованного клиента"""
    return APIClient()


@pytest.fixture()
def auth_client(client, user) -> APIClient:
    """вернет авторизованного клиента"""
    client.force_login(user)
    return client


@pytest.fixture
def user(db):
    user = User.objects.create_user(
        username='test_name',
        password='test_name123AS'
    )
    return user
