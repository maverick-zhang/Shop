from django.shortcuts import render
from rest_framework.mixins import DestroyModelMixin, CreateModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet

from user_operation.models import UserFav
from user_operation.serializer import UserFavSerializer


class UserFavViewSet(GenericViewSet, CreateModelMixin, DestroyModelMixin, ListModelMixin):
    """
    用户收藏功能
    """
    queryset = UserFav.objects.all()
    serializer_class = UserFavSerializer
