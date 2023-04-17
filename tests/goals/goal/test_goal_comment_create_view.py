import pytest
from django.urls import reverse

from goals.serializers.goal_comment import GoalCommentSerializer
from tests import factories


@pytest.mark.django_db
def test_create(auth_client, user, goal):
    response = auth_client.post(reverse('goal_comment_create'),
                                data={'text': 'test comment', 'goal': goal.pk})

    expected_response = {'id': response.data.get('id'),
                         'created': response.data.get('created'),
                         'updated': response.data.get('updated'),
                         'text': 'test comment',
                         'goal': goal.pk}

    assert response.status_code == 201
    assert response.data == expected_response


@pytest.mark.django_db
def test_list(auth_client, user, goal):
    comments = factories.CommentFactory.create_batch(5, goal=goal, user=user)
    response = auth_client.get(reverse('get_goal_comment_list'))
    expected_response = GoalCommentSerializer(instance=comments, many=True).data
    expected_response = sorted(expected_response, key=lambda x: x['id'], reverse=True)

    assert response.status_code == 200
    assert response.data == expected_response