# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0007_auto_20150703_1122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='slug',
            field=models.SlugField(default='dROybABYAv', max_length=10),
        ),
        migrations.AlterField(
            model_name='todolist',
            name='slug',
            field=models.SlugField(default='xwoPapocs5', max_length=10, null=True, blank=True),
        ),
    ]
