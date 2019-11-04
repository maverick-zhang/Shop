import re
from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator

from Shop.settings import REGEX_MOBIL
from user.models import VerifyCode

User = get_user_model()


class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, mobile):
        """
        验证手机号码
        :param mobil:手机号
        :return:手机号
        """
        # 验证手机号是否已经注册
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("用户已经存在")

        # 验证格式是否正确
        if not re.match(REGEX_MOBIL, mobile):
            raise serializers.ValidationError("手机号格式不正确")

        # 验证验证码发送频率
        one_minutes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if User.objects.filter(mobile=mobile, add_time__gt=one_minutes_ago):
            raise serializers.ValidationError("距离上一次发送未超过60s")

        return mobile


class UserRegSerializer(ModelSerializer):
    code = serializers.CharField(max_length=4, min_length=4, required=True, label="验证码", write_only=True,
                                 error_messages={
                                     "required": "请输入验证码",
                                     "blank": "请输入验证码",
                                     "max_length": "验证码格式错误",
                                     "min_length": "验证码格式错误",
                                 })
    username = serializers.CharField(required=True, allow_blank=False, label="用户名",
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="用户已存在"), ])

    password = serializers.CharField(required=True, label="密码", write_only=True,
                                     style={"input_type": "password"})

    def validated_code(self, code):
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data["username"]).order_by("-add_time")
        if verify_records:
            last_record = verify_records[0]
            five_minutes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            if five_minutes_ago > last_record.add_time:
                raise serializers.ValidationError("验证码过期")
            if last_record.code != code:
                raise serializers.ValidationError("验证码错误")
        else:
            raise serializers.ValidationError("验证码错误")

    def validate(self, attrs):
        attrs["mobile"] = attrs["username"]
        del attrs["code"]
        return attrs

    def create(self, validated_data):
        user = super(UserRegSerializer, self).create(validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    class Meta:
        model = User
        # fields必须包含传入的所有数据，然后进行映射
        fields = ('username', 'password', 'code')


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'birthday', 'mobile', 'gender')


