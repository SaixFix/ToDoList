from typing import Callable
from unittest.mock import ANY

import pytest
from django.urls import reverse
from rest_framework import status

from goals.models.board import Board, BoardParticipant


@pytest.fixture()
def board_create_data(faker) -> Callable:
    def _wrapper(**kwargs) -> dict:
        data = {'title': faker.sentence(2)}
        data |= kwargs
        return data

    return _wrapper


@pytest.mark.django_db()
class TestBoardCreate:
    url = reverse('board_create')

    def test_auth_required(self, client, board_create_data):
        """
        Неавторизованный пользователь при создание доски получит ошибку авторизации 403
        """
        response = client.post(self.url, data=board_create_data())

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_failed_to_create_deleted_board(self, auth_client, board_create_data):
        """
        При создание доски нельзя указать флаг is_deleted=True
        """
        response = auth_client.post(self.url, data=board_create_data(is_deleted=True))

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == self._serialize_board_response(is_deleted=False)
        assert Board.objects.last().is_deleted is False

    def test_request_user_became_board_owner(self, auth_client, user, board_create_data):
        """
        При создание доски пользователь становится владельцем
        """
        response = auth_client.post(self.url, data=board_create_data())

        assert response.status_code == status.HTTP_201_CREATED
        board_participant = BoardParticipant.objects.get(user_id=user.id)
        assert board_participant.board_id == response.data['id']
        assert board_participant.role == BoardParticipant.Role.owner

    def _serialize_board_response(self, **kwargs) -> dict:
        data = {
            'id': ANY,
            'created': ANY,
            'updated': ANY,
            'title': ANY,
            'is_deleted': False
        }
        data |= kwargs
        return data
