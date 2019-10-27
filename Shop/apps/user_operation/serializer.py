from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from user_operation.models import UserFav


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

