from django.shortcuts import render
from rest_framework.generics import CreateAPIView

from core.serializers import *


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
