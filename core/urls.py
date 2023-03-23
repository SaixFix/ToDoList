from django.urls import path, include

from core.views import *

urlpatterns = [
    path('signup/', UserCreateView.as_view(), name='create_user'),
]