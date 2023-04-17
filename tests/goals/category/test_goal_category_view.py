

import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db()
class TestBoardRetrieveView:

    @pytest.fixture(autouse=True)  # autouse будет вызываться заного каждый тест
    def setup(self, goal_category):
        """
        на каждый тест мы создаем участника с доской
        """
        self.url = self.get_url(goal_category.id)

    @staticmethod
    def get_url(category_pk: int) -> str:
        return reverse('get_goal_category_by_pk_and_RUD', kwargs={'pk': category_pk})

    def test_auth_required(self, client):
        """
        Неавторизованный пользователь не может просматривать доски, ошибка 403
        """
        response = client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN


    def test_failed_to_retrieve_deleted_board(self, auth_client, goal_category):
        """
        Автоизованный пользователь owner не может увидеть категорию с is_deleted = True
        """
        goal_category.is_deleted = True
        goal_category.save()

        response = auth_client.get(self.url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_auth_required(self, client):
        """
        Неавторизованный пользователь при удалении категории получит ошибку авторизации
        """

        response = client.delete(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
