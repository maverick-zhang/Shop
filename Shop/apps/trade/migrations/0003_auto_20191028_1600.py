# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-10-28 16:00
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0004_auto_20191022_1159'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('trade', '0002_auto_20191021_2110'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shoppingcart',
            old_name='goods_num',
            new_name='num',
        ),
        migrations.AlterUniqueTogether(
            name='shoppingcart',
            unique_together=set([('user', 'goods')]),
        ),
    ]
