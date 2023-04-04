from django.urls import path

from goals import views


urlpatterns = [
    path("goal_category/create", views.GoalCategoryCreateView.as_view(), name='goal_category create'),
    path("goal_category/list", views.GoalCategoryListView.as_view(), name='get goal_category list'),
    path(
        "goal_category/<pk>", views.GoalCategoryView.as_view(),
        name='get goal_category by pk and Retrieve Update Destroy'
        ),
    path("goal/create", views.GoalCreateView.as_view(), name='goal create'),
    path("goal/list", views.GoalListView.as_view(), name='get goal list'),
    path(
        "goal/<pk>", views.GoalView.as_view(),
        name='get goal by pk and Retrieve Update Destroy'
        ),
]