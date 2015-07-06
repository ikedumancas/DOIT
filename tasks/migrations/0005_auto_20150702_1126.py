# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_auto_20150702_1126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='slug',
            field=models.SlugField(default=b'testslug', max_length=10),
        ),
        migrations.AlterField(
            model_name='todolist',
            name='slug',
            field=models.SlugField(default=b'testslug', max_length=10),
        ),
    ]
