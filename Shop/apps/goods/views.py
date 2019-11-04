from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, mixins, generics
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_extensions.cache.mixins import CacheResponseMixin

from goods.filters import GoodsFilter
from goods.models import Goods, GoodsCategory, Banner
from goods.serializers import GoodsSerializer, CategorySerializer, BannerSerializer, IndexCategorySerializer


# class GoodsList(APIView):
#     """
#     list all goods
#     """
#     def get(self, requst):
#         goods = Goods.objects.all()[:10]
#         serializer = GoodsSerializer(goods, many=True)
#         return Response(serializer.data)
#
#     def post(self, requset):
#         serializer = GoodsSerializer(data=requset.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(requset.data, status=status.HTTP_201_CREATED)
#         return Response(status=status.HTTP_400_BAD_REQUEST)


class MyPaginator(PageNumberPagination):
    """
    定制自己的分页器类
    可以在具体的view类中指定分页器类，这样就不会使用全局默认的分页器
    """
    page_size = 12

    # 可以在url中自己指定参数
    page_query_param = "page"
    page_size_query_param = "page_size"

    max_page_size = 100


class GoodsListViewSet(CacheResponseMixin, GenericViewSet, ListModelMixin, RetrieveModelMixin):
    throttle_classes = (UserRateThrottle, AnonRateThrottle)
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    # 使用自己的分页器类进行分页
    pagination_class = MyPaginator
    filter_backends = (SearchFilter, DjangoFilterBackend, OrderingFilter)
    filter_class = GoodsFilter
    search_fields = ('name', 'goods_brief')
    ordering_fields = ('sold_num', 'shop_price')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.click_num += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CategoryViewSet(ListModelMixin, GenericViewSet, RetrieveModelMixin):
    """
    list:
        商品分类类列表数据
    detail:
        一个一级分类数据
    """

    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer


class BannerViewSet(ListModelMixin, GenericViewSet):
    """
    首页轮播图
    """
    queryset = Banner.objects.all().order_by("index")
    serializer_class = BannerSerializer


class IndexCategoryViewSet(ListModelMixin, GenericViewSet):
    """
    首页商品列表
    """
    # 这里获得的都是一类目录
    queryset = GoodsCategory.objects.filter(is_tab=True, name__in=("生鲜食品", "酒水饮料"))
    serializer_class = IndexCategorySerializer





