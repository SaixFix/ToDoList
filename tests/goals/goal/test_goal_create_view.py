import factory.django
import pytest
from django.urls import reverse
from rest_framework import status
from django.utils import timezone






@pytest.mark.django_db()
class TestCategoryCreateView:
    url = reverse('goal_create')
    now = timezone.now()

    @pytest.fixture(autouse=True)  # autouse будет вызываться заного каждый тест
    def setup(self, goal_category):
        """
        на каждый тест мы создаем участника с доской и категорией
        """

    def test_create_category(self, auth_client, goal_category):
        """
        Создание цели авторизованным юзером 201
        """
        response = auth_client.post(self.url, data=self._goal_create_data(category=goal_category.pk))

        assert response.status_code == status.HTTP_201_CREATED

    # def test_auth_required(self, client):
    #     """
    #     Неавторизованный пользователь при создании категории получит ошибку, 403
    #     """
    #     response = client.post(self.url, data=self._category_create_data())
    #     assert response.status_code == status.HTTP_403_FORBIDDEN
    #
    # def test_failed_to_create_deleted_category(self, auth_client, board):
    #     """
    #     При создание категории нельзя указать флаг is_deleted=True
    #     """
    #     response = auth_client.post(self.url, data=self._category_create_data(board=board.pk, is_deleted=True))
    #
    #     assert response.status_code == status.HTTP_201_CREATED
    #     assert response.json()['is_deleted'] is False

    def _goal_create_data(self, **kwargs) -> dict:
        data = {
            'title': 'asdasd',
            'description': 'asdasdasd',
            'due_date': self.now,
            'status': 1,
            'priority': 1
        }
        data |= kwargs
        return data
