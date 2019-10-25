from rest_framework import serializers

from user_operation.models import UserFav


class UserFavSerializer(serializers.ModelSerializer):
    # 由于用户是前端提供的，因此这里的user使用默认值，不需要在传入的dict中提供
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        model = UserFav
        fields = ("user", "goods")

