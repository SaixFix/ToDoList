from django.urls import reverse
from rest_framework import status

import pytest

from goals.models.board import BoardParticipant


@pytest.mark.django_db()
class TestBoardRetrieveView:

    @pytest.fixture(autouse=True)  # autouse будет вызываться заного каждый тест
    def setup(self, board_participant):
        """
        на каждый тест мы создаем участника с доской
        """
        self.url = self.get_url(board_participant.board_id)

    @staticmethod
    def get_url(board_pk: int) -> str:
        return reverse('get_goal_comment_by_pk_and_RUD', kwargs={'pk': board_pk})

    def test_auth_required(self, client):
        """
        Неавторизованный пользователь не может просматривать доски, ошибка 403
        """
        response = client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_failed_to_retrieve_deleted_board(self, auth_client, board):
        """
        Автоизованный пользователь owner не может увидеть доску с is_deleted = True
        """
        board.is_deleted = True
        board.save()

        response = auth_client.get(self.url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_failed_to_retrieve_foreign_board(self, client, user_factory):
        """
        Автоизованный пользователь не может увидеть чужую доску 403
        """
        another_user = user_factory.create()
        client.force_login(another_user)

        response = client.get(self.url)

        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db()
class TestBoardDestroyView:

    @pytest.fixture(autouse=True)  # autouse будет вызываться заного каждый тест
    def setup(self, board_participant):
        """
        на каждый тест мы создаем участника с доской
        """
        self.url = self.get_url(board_participant.board_id)

    @staticmethod
    def get_url(board_pk: int) -> str:
        return reverse('get_goal_comment_by_pk_and_RUD', kwargs={'pk': board_pk})

    def test_auth_required(self, client):
        """
        Неавторизованный пользователь не может удалять доски, ошибка 403
        """
        response = client.delete(self.url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.parametrize('role', [
        BoardParticipant.Role.writer,
        BoardParticipant.Role.reader
    ], ids=['writer', 'reader'])  # ids в результатах покажет название а не id
    def test_not_owner_failed_to_delete_board(self, client, user_factory, board, board_participant_factory, role):
        """
        Авторизованный клиент не owner, не может удалять чужие доски, 403
        """
        another_user = user_factory.create()
        board_participant_factory.create(user=another_user, board=board, role=role)
        client.force_login(another_user)

        response = client.delete(self.url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_owner_can_to_delete_board(self, auth_client, board):
        """
        Авторизованный клиент owner, может удалить свою доску, 204
        """
        response = auth_client.delete(self.url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        board.refresh_from_db()
        board.is_deleted is True
