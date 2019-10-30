import random
import time

from rest_framework import serializers

from goods.models import Goods
from goods.serializers import GoodsSerializer
from trade.models import ShoppingCart, OrderInfo, OrderGoods


class ShoppingCartDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False)

    class Meta:
        model = ShoppingCart
        fields = "__all__"


class ShoppingCartListSerializer(serializers.Serializer):
    """
    这里购物车要处理的逻辑比较复杂，需要重写字段的验证，因此使用Serializer，而不是ModelSerializer
    """
    goods = serializers.PrimaryKeyRelatedField(queryset=Goods.objects.all(), required=True)
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
        instance.num = validated_data["num"]
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





