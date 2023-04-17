
import factory.django
import pytest
from django.urls import reverse
from rest_framework import status






@pytest.mark.django_db()
class TestCategoryCreateView:
    url = reverse('goal_category_create')

    @pytest.fixture(autouse=True)  # autouse будет вызываться заного каждый тест
    def setup(self, board_participant):
        """
        на каждый тест мы создаем участника с доской
        """

    def test_create_category(self, auth_client, board):
        """
        Создание доски авторизованным юзером 201
        """
        response = auth_client.post(self.url, data=self._category_create_data(board=board.pk))

        assert response.status_code == status.HTTP_201_CREATED

    def test_auth_required(self, client):
        """
        Неавторизованный пользователь при создании категории получит ошибку, 403
        """
        response = client.post(self.url, data=self._category_create_data())
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_failed_to_create_deleted_category(self, auth_client, board):
        """
        При создание категории нельзя указать флаг is_deleted=True
        """
        response = auth_client.post(self.url, data=self._category_create_data(board=board.pk, is_deleted=True))

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()['is_deleted'] is False

    def _category_create_data(self, **kwargs) -> dict:
        data = {'title': factory.Faker('sentence')}
        data |= kwargs
        return data
