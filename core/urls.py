from django.urls import path, include

from core.views import *

urlpatterns = [
    path('create/', UserCreateView.as_view(), name='create_user'),
    path('', include('rest_framework.urls')),
]