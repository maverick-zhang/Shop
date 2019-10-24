import re
from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"


class SmsSerializer(serializers.Serializer):
    mobil = serializers.CharField(max_length=11)

    def validate_mobil(self, mobil):
        """
        验证手机号码
        :param mobil:手机号
        :return:手机哈
        """
        # 验证手机号是否已经注册
        if User.objects.filter(mobil=mobil).count():
            raise serializers.ValidationError("用户已经存在")

        # 验证格式是否正确
        if not re.match(REGEX_MOBILE, mobil):
            raise serializers.ValidationError("手机号格式不正确")

        # 验证验证码发送频率
        one_minutes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if User.objects.filter(mobil=mobil, add_time__gt=one_minutes_ago):
            raise serializers.ValidationError("距离上一次发送未超过60s")

        return mobil


