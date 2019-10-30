from django.shortcuts import render
from rest_framework.authentication import SessionAuthentication
from rest_framework.mixins import DestroyModelMixin, CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from trade.models import ShoppingCart, OrderInfo, OrderGoods
from trade.serializers import ShoppingCartListSerializer, ShoppingCartDetailSerializer, OrderInfoSerializer, \
    OrderDetailSerializer
from utils.permissions import IsOwnerOrReadOnly


class ShoppingCartViewSet(ModelViewSet):
    """
    list:
        购物车列表
    create:
        添加至购物车
    retrieve:
        获取单个记录
    destroy:
        删除某条记录
    """
    # queryset = ShoppingCart.objects.all()
    # serializer_class = ShoppingCartListSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    lookup_field = "goods_id"

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return ShoppingCartListSerializer
        elif self.action == "retrieve":
            return ShoppingCartDetailSerializer
        return ShoppingCartDetailSerializer


class OrderViewSet(GenericViewSet, ListModelMixin, CreateModelMixin,
                   DestroyModelMixin, RetrieveModelMixin):
    """
    list:
        订单列表
    create:
        创建订单
    delete:
        删除订单
    retrieve:
        获取订单详情
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    # serializer_class = OrderInfoSerializer

    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return OrderInfoSerializer
        elif self.action == "retrieve":
            return OrderDetailSerializer
        return OrderInfoSerializer

    def perform_create(self, serializer):
        """
        这一步主要进行进行序列化的保存（serializer.save()），可以在保存前增加一些自定义的操作
        :param serializer:
        :return:
        """
        order = serializer.save()
        shopping_carts = ShoppingCart.objects.filter(user=self.request.user)
        for shopping_cart in shopping_carts:
            order_goods = OrderGoods()
            order_goods.goods = shopping_cart.goods
            order_goods.goods_num = shopping_cart.nums
            order_goods.order = order
            order_goods.save()
            shopping_cart.delete()
        return order

