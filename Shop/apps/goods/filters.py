from django.db.models import Q
from django_filters.rest_framework import FilterSet, NumberFilter, CharFilter

from goods.models import Goods


class GoodsFilter(FilterSet):
    """
    商品的过滤
    """
    pricemin = NumberFilter(field_name="shop_price", lookup_expr="gte")
    pricemax = NumberFilter(field_name="shop_price", lookup_expr="lte")
    # icontaon代表模糊查询且不区分大小写，类似于SQL中的like
    # name = CharFilter(field_name="name", lookup_expr="icontains")
    top_category = NumberFilter(method="top_category_filter")

    def top_category_filter(self, queryset, name, value):
        """
        对传入的category_id进行向上查询获取到其所属的一级分类的category_id
        :param queryset:
        :param name:
        :param value: category_id
        :return:
        """
        return queryset.filter(Q(category_id=value) | Q(category__parent_category_id=value) |
                               Q(category__parent_category__parent_category_id=value))

    class Meta:
        model = Goods
        fields = ("pricemin", "pricemax", "name", "is_hot")
