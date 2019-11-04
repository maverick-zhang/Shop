from django.db.models import Q
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

from goods.models import Goods, GoodsCategory, GoodsImage, Banner, GoodsCategoryBrand, IndexAds


class CategorySerializer3(serializers.ModelSerializer):
    """
    第三级分类
    """

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class CategorySerializer2(serializers.ModelSerializer):
    """
    第二级分类
    """
    # 在model中定义的外键， related_name=sub_cat, 在这里通过一对多的关系从父类获取到子类
    sub_cat = CategorySerializer3(many=True)

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    """
    第一级分类
    """
    sub_cat = CategorySerializer2(many=True)

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class GoodsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsImage
        fields = ("image",)


class GoodsSerializer(serializers.ModelSerializer):
    # 通过显示定义具体字段的序列化对象，可以把外键的详细信息全部展示，否则外键只展示id
    category = CategorySerializer()
    images = GoodsImageSerializer(many=True)

    class Meta:
        model = Goods
        # fields = ("name", "category", "add_time")
        # 使用一下方式快速实现全部导入
        fields = "__all__"


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = "__all__"


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategoryBrand
        fields = "__all__"


class IndexCategorySerializer(serializers.ModelSerializer):
    brands = BrandSerializer(many=True)
    goods = serializers.SerializerMethodField(read_only=True)
    # 由于query_set中已经指定了获取的是一级类目，所以这里的sub_cat是二级类目
    sub_cat = CategorySerializer2(many=True)
    ad_goods = serializers.SerializerMethodField(read_only=True)

    def get_ad_goods(self, obj):
        goods_ins_dict = {}
        all_goods = IndexAds.objects.filter(category_id=obj.id)
        if all_goods:
            goods_ins = all_goods[0].goods
            # 添加context之后，序列化时，会自动把image字段前面添加域名，否则将只有路径
            # 当在serializer中嵌套serializer时会出现这种问题
            goods_ins_dict = GoodsSerializer(goods_ins, many=False, context={"request": self.context["request"]}).data
        return goods_ins_dict

    def get_goods(self, obj):
        """
        首先从传入的category实例中获取到当前所属的类，然后通过filter获取到该目录所属的一级目录下的所有商品实例
        然后进行序列化，以json的格式作为goods字段的value。
        :param obj:
        :return:
        """
        all_goods = Goods.objects.filter(Q(category_id=obj.id) | Q(category__parent_category_id=obj.id) |
                                         Q(category__parent_category__parent_category_id=obj.id))
        # 添加context之后，序列化时，会自动把image字段前面添加域名，否则将只有路径
        # 当在serializer中嵌套serializer时会出现这种问题
        goods_serializer = GoodsSerializer(all_goods, many=True, context={"request": self.context["request"]})
        return goods_serializer.data

    class Meta:
        model = GoodsCategory
        fields = "__all__"
