from django.urls import path

from goals import views


urlpatterns = [
    path("goal_category/create", views.GoalCategoryCreateView.as_view(), name='GoalCategoryCreate'),
    path("goal_category/list", views.GoalCategoryListView.as_view(), name='GoalCategoryList'),
    path("goal_category/<pk>", views.GoalCategoryView.as_view()),
]