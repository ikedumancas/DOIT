# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_auto_20150702_1126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='slug',
            field=models.SlugField(default='Dlx2Wds74U', max_length=10),
        ),
        migrations.AlterField(
            model_name='todolist',
            name='slug',
            field=models.SlugField(default='18JYldKPG3', max_length=10),
        ),
    ]
