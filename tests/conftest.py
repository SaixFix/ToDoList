import pytest
from rest_framework.test import APIClient

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
