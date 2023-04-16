import pytest
from django.urls import reverse

from goals.models.board import Board

from goals.serializers.board import BoardCreateSerializer




# @pytest.mark.django_db
# def test_board_list(auth_client, new_user):
#     board_list = BoardFactory.create_batch(4)
#
#     response = auth_client.get(f"{reverse('board_list')}?limit=5")
#
#     expected_response = {
#         "count": 4,
#         "next": None,
#         "previous": None,
#         "results": BoardCreateSerializer(instance=boards, many=True).data
#     }
