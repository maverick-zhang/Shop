from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models

from goods.models import Goods

User = get_user_model()


class UserFav(models.Model):
    """
    用户收藏
    """
    user = models.ForeignKey(User, verbose_name="用户")
    goods = models.ForeignKey(Goods,verbose_name="商品")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "用户收藏"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.name


class UserLeavingMessage(models.Model):
    """
    用户留言
    """
    MESSAGE_TYPE = (
        (1, "留言"),
        (2, "投诉"),
        (3, "询问"),
        (4, "售后"),
        (5, "求购"),
    )
    user = models.ForeignKey(User, verbose_name="用户")
    msg_type = models.CharField(choices=MESSAGE_TYPE, verbose_name="留言类型",
                                help_text="留言类型：1(留言), 2(投诉), 3(询问), 4(售后), 5(求购)", max_length=8)
    message = models.TextField(default="", verbose_name="留言内容", help_text="留言内容")
    file = models.FileField(upload_to="", verbose_name="上传的文件", help_text="上传的文件")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    subject = models.CharField(max_length=100, default="", verbose_name="主题")

    class Meta:
        verbose_name = "用户留言"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.name


class UserAddress(models.Model):
    """
    用户地址
    """
    user = models.ForeignKey(User, verbose_name="用户")
    address = models.CharField(max_length=100, default="", verbose_name="详细地址")
    district = models.CharField(max_length=100, default="", verbose_name="区域")
    singer_name = models.CharField(max_length=30, default="", verbose_name="签收人")
    singer_mobil = models.CharField(max_length=16, default="", verbose_name="电话")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "用户地址"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.address

