import json

from django.core import serializers
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.views.generic.base import View

from goods.models import Goods


class GoodsListView(View):
    """
    这里使用的是django内置的View类，是CBV的模式
    """

    def get(self, request):
        """
        通过django的View实现商品列表页
        :param request:
        :return:
        """
        json_list = []
        goods = Goods.objects.all()[:10]
        for good in goods:
            # 手动进行序列化
            # 被序列化的value不能是类，应该是json支持的格式如字符串或者数字
            # json_dict = {"name": good.name, "category": good.category.name, "market_price": good.market_price}
            # json_list.append(json_dict)

            # 使用django内置的序列化方法进行序列化
            # 但是ImageFieldFile不能使用正确序列化
            # json_dict = model_to_dict(good)
            # json_list.append(json_dict)
            pass

        # 使用django内置的serializers模块中的serialize方法(注意名字)
        json_data = serializers.serialize("json", goods)
        # print(type(json_data))
        # print(json_data)
        # json_data = json.loads(json_data)   # loads方法把json格式转为python对象，在这里不需要这个转换

        # 注意这里使用的是dumps方法，而不是dump，序列化为一个文件，前者序列化为stream，在HttpResponse中要使用前者
        # return HttpResponse(json.dumps(json_list), content_type="application/json")
        return HttpResponse(json_data, content_type="application/json")

        # 如果要传递非完全json的格式文件，需要把safe=False开启
        # In order to allow non-dict objects to be serialized set the safe parameter to False.
        # return JsonResponse(json_data, safe=False)