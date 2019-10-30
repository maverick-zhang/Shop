from datetime import datetime

from django.db import models
from django.contrib.auth import get_user_model

# 通过该函数可以直接把在settings中注册的user模型找到
from goods.models import Goods

User = get_user_model()


class ShoppingCart(models.Model):
    """
    购物车
    """
    user = models.ForeignKey(User, verbose_name="用户")
    goods = models.ForeignKey(Goods, verbose_name="商品")
    nums = models.IntegerField(default=0, verbose_name="购买数量")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "购物车"
        verbose_name_plural = verbose_name
        unique_together = ("user", "goods")

    def __str__(self):
        return "{0}({1:d})".format(self.goods.name, self.nums)


class OrderInfo(models.Model):
    """
    订单信息
    """
    ORDER_STATUS = (
        ("success", "成功"),
        ("cancel", "取消"),
        ("paying", "待支付"),
    )
    # PAY_TYPE = (
    #     ("alipay", "支付宝"),
    #     ("wechat", "微信"),
    # )

    user = models.ForeignKey(User, verbose_name="用户")
    order_sn = models.CharField(max_length=30, null=True, blank=True, unique=True, verbose_name="订单号")
    trade_no = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name="交易编号")
    pay_status = models.CharField(choices=ORDER_STATUS, default="paying", max_length=10, verbose_name="支付状态")
    order_mount = models.FloatField(default=0, verbose_name="订单金额")
    pay_time = models.DateTimeField(null=True, blank=True, verbose_name="支付时间")
    post_script = models.CharField(max_length=200, verbose_name="订单留言", default="")
    # pay_type = models.CharField(max_length=10, choices=PAY_TYPE, verbose_name="支付方式")

    # 收货人的信息
    address = models.CharField(max_length=100, verbose_name="收货地址", default="")    # 这里不使用地址外键的原因是这里的信息不能进行修改两者是隔离的
    signer_name = models.CharField(max_length=20, default="", verbose_name="签收人" )
    signer_mobil = models.CharField(max_length=16, verbose_name="联系电话", default="")

    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "订单"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.order_sn


class OrderGoods(models.Model):
    """
    订单商品详情
    """
    order = models.ForeignKey(OrderInfo, verbose_name="订单信息", related_name="goods")
    goods = models.ForeignKey(Goods, verbose_name="订单商品")
    goods_num = models.IntegerField(default=0, verbose_name="商品数量")

    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "订单商品"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name

