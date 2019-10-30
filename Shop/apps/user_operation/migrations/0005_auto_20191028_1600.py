# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-10-28 16:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_operation', '0004_auto_20191028_1154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraddress',
            name='address',
            field=models.CharField(default='', help_text='详细地址', max_length=100, verbose_name='详细地址'),
        ),
        migrations.AlterField(
            model_name='useraddress',
            name='city',
            field=models.CharField(default='', help_text='城市', max_length=100, verbose_name='城市'),
        ),
        migrations.AlterField(
            model_name='useraddress',
            name='district',
            field=models.CharField(default='', help_text='区域', max_length=100, verbose_name='区域'),
        ),
        migrations.AlterField(
            model_name='useraddress',
            name='province',
            field=models.CharField(default='', help_text='省份', max_length=100, verbose_name='省份'),
        ),
        migrations.AlterField(
            model_name='useraddress',
            name='signer_mobil',
            field=models.CharField(default='', help_text='联系电话', max_length=16, verbose_name='电话'),
        ),
        migrations.AlterField(
            model_name='useraddress',
            name='signer_name',
            field=models.CharField(default='', help_text='签收人', max_length=30, verbose_name='签收人'),
        ),
    ]
