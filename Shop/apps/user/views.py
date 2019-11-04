import random

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler

from user.models import VerifyCode
from user.serializers import SmsSerializer, UserRegSerializer, UserDetailSerializer
from utils.yunpian import YunPian

User = get_user_model()

API_KEY = "TEST"


class CustomBackend(ModelBackend):
    """
    自定义用户验证后端类
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(mobile=username))
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

        mobile = serializer.validated_data["mobile"]

        yun_pian = YunPian(API_KEY)
        code = self.generate_code()
        sms_status = yun_pian.send_sms(code, mobile)
        if sms_status["code"] != 0:
            code_record = VerifyCode(code=code, mobile=mobile)
            code_record.save()
            data = {
                "mobile": sms_status["msg"]
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"mobile": mobile}, status=status.HTTP_201_CREATED)


class UserViewSet(CreateModelMixin, GenericViewSet, RetrieveModelMixin, UpdateModelMixin):
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    # serializer_class = UserRegSerializer
    # 不同的action需要的permission不同，因此不能定义视图类的全局权限类
    # permission_classes = (IsAuthenticated, )
    queryset = User.objects.all()

    def get_permissions(self):
        """
        注意这里的返回结果需要是认证类的实例列表
        :return:
        """
        if self.action == "create":
            return [AllowAny(), ]
        elif self.action == "retrieve":
            return [IsAuthenticated(), ]
        else:
            return []

    def get_serializer_class(self):
        if self.action == "create":
            return UserRegSerializer
        elif self.action == "retrieve":
            return UserDetailSerializer
        return UserDetailSerializer

    def create(self, request, *args, **kwargs):
        """
        重载create方法（copy原有的create方法，进行增量操作），在创建用户成功之后（即成功注册之后，返回一个jwt，让用户直接登录）
        通过perform_create获取到用户实例，使用jwt_pay_load_handler(usr)生成负载，再用jwt_encode_handler(payload)
        得到最终的jwt，添加到要返回的字典当中，最后返回。
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict["token"] = jwt_encode_handler(payload)
        re_dict["name"] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()

    def get_object(self):
        return self.request.user










