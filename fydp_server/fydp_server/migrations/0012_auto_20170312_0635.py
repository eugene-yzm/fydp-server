# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-12 06:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fydp_server', '0011_auto_20170312_0634'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cycle',
            name='end_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
