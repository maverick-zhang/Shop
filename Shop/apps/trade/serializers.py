import random
import time

from rest_framework import serializers

from Shop.settings import HOST_IP, PRIVATE_KEY_PATH, ALIPAY_PUBLIC_KEY_PATH
from goods.models import Goods
from goods.serializers import GoodsSerializer
from trade.models import ShoppingCart, OrderInfo, OrderGoods
from utils.alipay import AliPay


class ShoppingCartSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False)

    class Meta:
        model = ShoppingCart
        fields = "__all__"


class ShoppingUpdateCreateSerializer(serializers.Serializer):
    """
    这里购物车要处理的逻辑比较复杂，需要重写字段的验证，因此使用Serializer，而不是ModelSerializer
    """
    goods = serializers.PrimaryKeyRelatedField(queryset=Goods.objects.all(), many=False)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    nums = serializers.IntegerField(required=True, min_value=1,
                                    error_messages={
                                       "min_value": "购买的数量必须大于一",
                                       "required": "请选择购买数量",
                                    })

    def create(self, validated_data):
        user = self.context["request"].user
        nums = validated_data["nums"]
        # 注意此时goods已经反序列化为Goods对象
        goods = validated_data["goods"]

        existed = ShoppingCart.objects.filter(user=user, goods=goods)
        if existed:
            existed_item = existed[0]
            existed_item.nums += nums
            existed_item.save()
            return existed_item
        else:
            # new_cart_item = ShoppingCart()
            # new_cart_item.goods = goods
            # new_cart_item.num = num
            # new_cart_item.user = user
            # new_cart_item.save()
            # 下面的语句一步搞定！注意validated_data需要要unpack
            new_cart_item = ShoppingCart.objects.create(**validated_data)
            return new_cart_item

    def update(self, instance, validated_data):
        instance.nums = validated_data["nums"]
        instance.save()


class OrderGoodsSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False)

    class Meta:
        model = OrderGoods
        fields = "__all__"


class OrderDetailSerializer(serializers.ModelSerializer):
    goods = OrderGoodsSerializer(many=True)

    class Meta:
        model = OrderInfo
        fields = "__all__"


class OrderInfoSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    pay_status = serializers.CharField(read_only=True)
    order_sn = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    pay_time = serializers.DateTimeField(read_only=True)
    alipay_url = serializers.SerializerMethodField(read_only=True)

    def get_alipay_url(self, obj):
        alipay = AliPay(
            appid="2016101600703402",
            app_notify_url="http://192.168.1.5:8000/alipay/return/",
            app_private_key_path=PRIVATE_KEY_PATH,
            alipay_public_key_path=ALIPAY_PUBLIC_KEY_PATH,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://192.168.1.5:8000/alipay/return/"
        )

        url = alipay.direct_pay(
            subject=obj.order_sn,
            out_trade_no=obj.order_sn,
            total_amount=obj.order_amount
        )
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)
        return re_url

    def generate_order_sn(self):
        """
        生成订单号的主要方式为：时间+用户名+随机数
        :return:
        """
        order_sn = "{time_str}{user_id}{random_str}".format(time_str=time.strftime("%Y%m%d%H%M%S"),
                                                            user_id=self.context["request"].user.id,
                                                            random_str=random.randint(10, 99))
        return order_sn

    def validate(self, attrs):
        attrs["order_sn"] = self.generate_order_sn()
        return attrs

    class Meta:
        model = OrderInfo
        fields = "__all__"





