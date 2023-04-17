import pytest
from rest_framework.test import APIClient

from core.models import User
from goals.models.board import BoardParticipant
from goals.models.goal import Goal
from goals.models.goal_category import GoalCategory
from goals.models.goal_comment import GoalComment
from tests import factories

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


@pytest.fixture
def board():
    board = factories.BoardFactory.create()
    return board


@pytest.fixture
def participant(user, board):
    BoardParticipant.objects.create(user=user, board=board)


@pytest.fixture
def category(board, user, participant):
    category = GoalCategory.objects.create(board=board, user=user)
    return category


@pytest.fixture
def goal(category, user):
    goal = Goal.objects.create(category=category, user=user)
    return goal


@pytest.fixture
def comment(goal, new_user):
    comment = factories.CommentFactory.create(user=new_user, goal=goal)
    return comment
