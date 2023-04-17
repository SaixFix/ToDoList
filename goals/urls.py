from django.urls import path
from goals.views import goal_category, goal, goal_comment, board

urlpatterns = [
    # Goal category
    path("goal_category/create", goal_category.GoalCategoryCreateView.as_view(), name='goal_category_create'),
    path("goal_category/list", goal_category.GoalCategoryListView.as_view(), name='get goal_category list'),
    path(
        "goal_category/<pk>", goal_category.GoalCategoryView.as_view(),
        name='get_goal_category_by_pk_and_RUD'
        ),
    # Goal
    path("goal/create", goal.GoalCreateView.as_view(), name='goal_create'),
    path("goal/list", goal.GoalListView.as_view(), name='get goal list'),
    path(
        "goal/<pk>", goal.GoalView.as_view(),
        name='get goal by pk and Retrieve Update Destroy'
        ),
    # Goal comment
    path("goal_comment/create", goal_comment.GoalCommentCreateView.as_view(), name='goal_comment create'),
    path("goal_comment/list", goal_comment.GoalCommentListView.as_view(), name='get goal_comment list'),
    path(
        "goal_comment/<pk>", goal_comment.GoalCommentView.as_view(),
        name='get goal_comment by pk and Retrieve Update Destroy'
        ),
    # Board
    path("board/create", board.BoardCreateView.as_view(), name='board_create'),
    path("board/list", board.BoardListView.as_view(), name='board_list_view'),
    path(
        "board/<pk>", board.BoardView.as_view(),
        name='get_goal_comment_by_pk_and_RUD'
        ),
]