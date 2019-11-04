from django.db.models.signals import post_delete
from django.dispatch import receiver

from user_operation.models import UserFav


@receiver(post_delete, sender=UserFav)
def delete_userfav(sender, instance=None, created=False, **kwargs):
    """
    使用信号量在对对象进行删除和创建时执行一些操作
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    goods = instance.goods
    goods.fav_num -= 1
    goods.save()