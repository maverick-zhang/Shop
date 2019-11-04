"""Shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from django.views.static import serve
from rest_framework.authtoken import views
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token

import xadmin
from Shop.settings import MEDIA_ROOT
from goods.views import GoodsListViewSet, CategoryViewSet, BannerViewSet, IndexCategoryViewSet

# from goods.views_base import GoodsListView
from trade.views import ShoppingCartViewSet, OrderViewSet, AliPayViewSet
from user.views import UserViewSet
from user_operation.views import UserFavViewSet, LeavingMessageViewSet, AddressViewSet

router = DefaultRouter()
# 商品列表
router.register(r'goods', GoodsListViewSet, base_name='goods')
# 商品分类
router.register(r'categorys', CategoryViewSet, base_name='categorys')
# 用户
router.register(r'users', UserViewSet, base_name='users')
# 用户收藏
router.register(r'userfavs', UserFavViewSet, base_name="userfav")
# 用户收藏
router.register(r'messages', LeavingMessageViewSet, base_name="messages")
# 收货地址
router.register(r'address', AddressViewSet, base_name="address")
# 购物车
router.register(r'shopcarts', ShoppingCartViewSet, base_name="shoppingcart")
# 订单管理
router.register(r'orders', OrderViewSet, base_name="orders")
# 首页轮播图
router.register(r'banners', BannerViewSet, base_name="banners")
# 首页商品列表
router.register(r'indexgoods', IndexCategoryViewSet, base_name="indexgoods")


urlpatterns = [
    # index页面
    url(r'^index/', TemplateView.as_view(template_name="index.html"), name="index"),

    url(r'^xadmin/', xadmin.site.urls),
    # 访问资源时配置的URL
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    # 商品的列表页面
    # url(r'^goods/$', GoodsListView.as_view(), name="goods_list"),
    url(r'^docs/', include_docs_urls(title="商店")),

    # DRF自带的token验证
    url(r'^api-token-auth/', views.obtain_auth_token),

    # jwt 验证
    url(r'^login/$', obtain_jwt_token),

    #  browsable API you'll probably also want to add REST framework's login and logout views
    url(r'^api-auth/', include('rest_framework.urls')),

    # url(r'^goods/$', GoodsList.as_view(), name="goods_list")

    # 支付宝的支付接口的return_url
    url(r'^alipay/return/', AliPayViewSet.as_view(), name="alipay_return"),

    # 第三方登录
    url('', include('social_django.urls', namespace='social')),

]
urlpatterns += router.urls