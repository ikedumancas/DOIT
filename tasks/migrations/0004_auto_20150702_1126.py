# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_todolist_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='todo',
            name='slug',
            field=models.SlugField(default=b'testslug', unique=True, max_length=10),
        ),
        migrations.AddField(
            model_name='todolist',
            name='slug',
            field=models.SlugField(default=b'testslug', unique=True, max_length=10),
        ),
    ]
