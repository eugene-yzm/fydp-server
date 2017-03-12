# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-12 06:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fydp_server', '0009_auto_20170307_0919'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cycle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('tag', models.CharField(blank=True, default=b'', max_length=100)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('recommendations', models.CharField(blank=True, default=b'', max_length=100)),
                ('done', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cycles', to='fydp_server.User')),
            ],
        ),
    ]
