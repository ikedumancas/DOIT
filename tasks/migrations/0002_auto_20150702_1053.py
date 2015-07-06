# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='todo',
            options={'ordering': ['order', 'timestamp'], 'verbose_name': 'Task', 'verbose_name_plural': 'Tasks'},
        ),
        migrations.AlterModelOptions(
            name='todolist',
            options={'ordering': ['order', 'timestamp'], 'verbose_name': 'Todo List', 'verbose_name_plural': 'Todo Lists'},
        ),
        migrations.AddField(
            model_name='todo',
            name='status',
            field=models.SlugField(default=b'active', max_length=10, choices=[(b'active', b'active'), (b'done', b'done'), (b'archived', b'archived')]),
        ),
        migrations.AddField(
            model_name='todolist',
            name='order',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
