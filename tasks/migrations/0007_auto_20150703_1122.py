# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0006_auto_20150703_0516'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='todolist',
            options={'ordering': ['timestamp'], 'verbose_name': 'Todo List', 'verbose_name_plural': 'Todo Lists'},
        ),
        migrations.RemoveField(
            model_name='todolist',
            name='order',
        ),
        migrations.AlterField(
            model_name='todo',
            name='slug',
            field=models.SlugField(default='eamXewiOG0', max_length=10),
        ),
        migrations.AlterField(
            model_name='todolist',
            name='slug',
            field=models.SlugField(default='O6kd3Qdkj2', max_length=10, null=True, blank=True),
        ),
    ]
