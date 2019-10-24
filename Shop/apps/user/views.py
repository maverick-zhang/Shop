import random

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from rest_framework import status
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from user.models import VerifyCode
from user.serializers import SmsSerializer
from utils.yunpian import YunPian

User = get_user_model()

API_KEY = "TEST"


class CustomBackend(ModelBackend):
    """
    自定义用户验证后端类
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(mobil=username))
        except User.DoesNotExist:
            return
        if user.check_password(password):
            return user
        else:
            return None


class SmsCodeViewSet(CreateModelMixin, GenericViewSet):
    serializer_class = SmsSerializer

    @staticmethod
    def generate_code():
        """
        随机生成4位验证码
        :return: 验证码
        """
        seeds = "0123456789"
        code_list = []
        for i in range(4):
            code_list.append(random.choice(seeds))
        return ''.join(code_list)

    def create(self, request, *args, **kwargs):
        serializer = request.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        mobil = serializer.validated_data["mobil"]

        yun_pian = YunPian(API_KEY)
        code = self.generate_code()
        sms_status = yun_pian.send_sms(code, mobil)
        if sms_status["code"] != 0:
            code_record = VerifyCode(code=code, mobil=mobil)
            code_record.save()
            data = {
                "mobil": sms_status["msg"]
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"mobil": mobil}, status=status.HTTP_201_CREATED)







