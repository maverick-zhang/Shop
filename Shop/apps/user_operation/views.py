from django.shortcuts import render
from rest_framework.authentication import SessionAuthentication
from rest_framework.mixins import DestroyModelMixin, CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from user_operation.models import UserFav
from user_operation.serializer import UserFavSerializer
from utils.permissions import IsOwnerOrReadOnly


class UserFavViewSet(GenericViewSet, CreateModelMixin,
                     DestroyModelMixin, ListModelMixin,
                     RetrieveModelMixin, ):
    """
    用户收藏功能
    """
    # 这里有两个权限认证，前者为是否为登录的用户，后者为是否是该数据库记录的拥有者，因为很明显只有本用户才可以进行删除自己的收藏
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    # 在重载了get_queryset()之后，就不需要在声明query_set了
    # queryset = UserFav.objects.all()
    serializer_class = UserFavSerializer
    # 默认使用的是pk，但是这里使用goods_id更合理，改完之后，url path上的id就将对应goods_id
    lookup_field = "goods_id"

    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)
