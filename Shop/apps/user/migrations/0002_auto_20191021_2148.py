# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-10-21 21:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='birthday',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='mobil',
            field=models.CharField(default='', max_length=16, verbose_name='电话'),
        ),
    ]