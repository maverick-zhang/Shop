# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-10-28 17:15
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0003_auto_20191028_1600'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shoppingcart',
            old_name='num',
            new_name='nums',
        ),
    ]