from django.urls import path, include

from core.views import *

urlpatterns = [
    path('signup', UserCreateView.as_view(), name='create_user'),
    path('login', LoginUserView.as_view(), name='login'),
    path('profile', UserRetrieveUpdateDestroyView.as_view(), name='profile'),
    path('update_password', PasswordChangeView.as_view(), name='change_password'),
]
