import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class UserProfile(AbstractUser):
    """
    用户
    """
    name = models.CharField(max_length=64, null=True, blank=True, verbose_name="姓名")
    email = models.CharField(max_length=64, null=True, blank=True, verbose_name="邮箱")
    mobil = models.CharField(max_length=16, verbose_name="电话", default="")
    gender = models.CharField(max_length=8, choices=(("male", "男"), ("female", "女")), default="female")
    birthday = models.DateField(null=True)
    add_time = models.DateTimeField(default=datetime.datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class VerifyCode(models.Model):
    """
    短信验证码
    """
    code = models.CharField(max_length=10, verbose_name="验证码")
    mobil = models.CharField(max_length=16, verbose_name="电话")
    add_time = models.DateTimeField(default=datetime.datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "短信验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code





