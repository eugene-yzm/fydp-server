# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-07 07:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fydp_server', '0007_user_data_post_key'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='data_post_key',
            new_name='access_data_key',
        ),
    ]
