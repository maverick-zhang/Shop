from django.shortcuts import render
from rest_framework.authentication import SessionAuthentication
from rest_framework.mixins import DestroyModelMixin, CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from user_operation.models import UserFav, UserLeavingMessage, UserAddress
from user_operation.serializer import UserFavSerializer, UserFavDetailSerializer, LeavingMessageSerializer, \
    AddressSerializer
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
    # serializer_class = UserFavSerializer
    # 默认使用的是pk，但是这里使用goods_id更合理，改完之后，url path上的id就将对应goods_id
    lookup_field = "goods_id"

    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        instance = serializer.save()
        goods = instance.goods
        goods.fav_num += 1
        goods.save()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserFavDetailSerializer
        elif self.action == "create":
            return UserFavSerializer
        return UserFavSerializer


class LeavingMessageViewSet(GenericViewSet, CreateModelMixin, ListModelMixin,
                            DestroyModelMixin, RetrieveModelMixin):

    """
    list:
        获取留言列表
    retrieve:
        获取留言详情
    destroy:
        删除留言
    """
    serializer_class = LeavingMessageSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return UserLeavingMessage.objects.filter(user=self.request.user)


class AddressViewSet(ModelViewSet):
    """
    收货地址管理
    list:
        地址列表
    retrieve:
        地址详情
    create:
        黄建地址
    destroy:
        删除地址
    update:
        修改地址
    """
    serializer_class = AddressSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)


