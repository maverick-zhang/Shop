# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-10-30 18:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20191021_2148'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='mobil',
            new_name='mobile',
        ),
        migrations.RenameField(
            model_name='verifycode',
            old_name='mobil',
            new_name='mobile',
        ),
    ]
