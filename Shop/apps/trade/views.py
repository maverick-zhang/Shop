from datetime import datetime

from django.shortcuts import render
from rest_framework.authentication import SessionAuthentication
from rest_framework.mixins import DestroyModelMixin, CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from Shop.settings import ALIPAY_PUBLIC_KEY_PATH, PRIVATE_KEY_PATH, HOST_IP
from trade.models import ShoppingCart, OrderInfo, OrderGoods
from trade.serializers import OrderInfoSerializer, OrderDetailSerializer, ShoppingUpdateCreateSerializer, \
    ShoppingCartSerializer
from utils.alipay import AliPay
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

    def perform_create(self, serializer):
        shopcart = serializer.save()
        # 创建时把商品的库存量进行修改
        goods = shopcart.goods
        goods.goods_num -= shopcart.nums
        goods.save()

    def perform_destroy(self, instance):
        # 注意perform_destroy传入的是对象，而perform_update和perform_create传入的都是序列化类的实例
        goods = instance.goods
        goods.goods_num += instance.nums
        instance.delete()
        goods.save()

    def perform_update(self, serializer):
        # instance是作为model的实例传入serializer里的
        existed_records = ShoppingCart.objects.get(id=serializer.instance.id)
        existed_nums = existed_records.nums
        shop_cart = serializer.save()
        nums = shop_cart.nums - existed_nums
        goods = shop_cart.goods
        goods.goods_num -= nums
        goods.save()

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return ShoppingCartSerializer
        elif self.action == "create":
            return ShoppingUpdateCreateSerializer
        elif self.action == "update":
            return ShoppingUpdateCreateSerializer
        return ShoppingCartSerializer


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


class AliPayViewSet(APIView):
    def get(self, request):
        """
        处理支付宝进行return_url的请求
        :param request:
        :return:
        """
        return Response("success")

    def post(self, request):
        """
        处理支付宝进行notify_url的请求
        :param request:
        :return:
        """
        processed_query = {}
        for key, value in request.POST.items:
            processed_query[key] = value
        sign = processed_query.pop("sign", None)

        alipay = AliPay(
            appid="2016101600703402",
            app_notify_url="http://"+HOST_IP+":8000/alipay/return/",
            app_private_key_path=PRIVATE_KEY_PATH,
            alipay_public_key_path=ALIPAY_PUBLIC_KEY_PATH,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://"+HOST_IP+":8000/alipay/return/"
        )

        verify_return = alipay.verify(processed_query, sign)
        if verify_return:
            order_sn = processed_query.get("out_trade_no", None)
            trade_no = processed_query.get("trade_no", None)
            order = OrderInfo.objects.filter(order_sn=order_sn)[0]
            for order_goods in order.goods:
                order_goods.goods.goods_num += order_goods.goods_num
                order_goods.goods.save()
            order.trade_no = trade_no
            order.trade_status = "TRADE_SUCCESS"
            order.pay_time = datetime.now()
            order.save()
            return Response("success")


