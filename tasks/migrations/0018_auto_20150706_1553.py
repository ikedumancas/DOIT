# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0017_auto_20150705_1618'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='status',
            field=models.SlugField(default=b'active', max_length=10, choices=[(b'active', b'Active'), (b'done', b'Done'), (b'archived', b'Archived')]),
        ),
        migrations.AlterField(
            model_name='todolist',
            name='status',
            field=models.SlugField(default=b'active', max_length=10, choices=[(b'active', b'Active'), (b'done', b'Done'), (b'archived', b'Archived')]),
        ),
    ]
