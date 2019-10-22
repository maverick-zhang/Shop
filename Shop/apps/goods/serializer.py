from rest_framework import serializers


# class GoodsSerializer(serializers.Serializer):
#     name = serializers.CharField(required=True, max_length=100)
#     goods_front_image = serializers.ImageField()
#
#     def create(self, validated_data):
#         pass
#
#     def update(self, instance, validated_data):
#         pass

from goods.models import Goods, GoodsCategory


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = "__all__"





class GoodsSerializer(serializers.ModelSerializer):
    # 通过显示定义具体字段的序列化对象，可以把外键的详细信息全部展示，否则外键只展示id
    category = CategorySerializer()

    class Meta:
        model = Goods
        fields = ("name", "category", "add_time")
        # 使用一下方式快速实现全部导入
        # fields = "__all__"
