import re

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.viewsets import ModelViewSet

from Shop.settings import REGEX_MOBIL
from goods.serializers import GoodsSerializer
from user_operation.models import UserFav, UserLeavingMessage, UserAddress


class UserFavSerializer(serializers.ModelSerializer):
    # 由于用户是前端提供的，因此这里的user使用默认值，不需要在传入的dict中提供
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = UserFav
        fields = ("user", "goods", "id")
        validators = [UniqueTogetherValidator(
            queryset=UserFav.objects.all(),
            fields=("user", "goods"),
            message="用户已收藏"
        )]


class UserFavDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer()

    class Meta:
        model = UserFav
        fields = ("id", "goods")


class LeavingMessageSerializer(serializers.ModelSerializer):
    # 由于用户是前端提供的，因此这里的user使用默认值，不需要在传入的dict中提供
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True)

    class Meta:
        model = UserLeavingMessage
        fields = ("user", "msg_type", "message", "file", "subject", "id", "add_time")


class AddressSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    def validate_signer_mobile(self, mobile):
        if not re.match(REGEX_MOBIL, mobile):
            raise serializers.ValidationError("手机号格式不正确")
        else:
            return mobile

    class Meta:
        model = UserAddress
        fields = ("user", "address", "signer_name", "signer_mobile", "district", "province", "city", "id")
