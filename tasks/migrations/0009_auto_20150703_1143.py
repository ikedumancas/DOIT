# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0008_auto_20150703_1141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='slug',
            field=models.SlugField(default='C9fjxOwuVN', max_length=10),
        ),
        migrations.AlterField(
            model_name='todolist',
            name='slug',
            field=models.SlugField(max_length=10, null=True, blank=True),
        ),
    ]
