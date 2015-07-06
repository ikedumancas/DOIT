# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0011_auto_20150703_1215'),
    ]

    operations = [
        migrations.AddField(
            model_name='todolist',
            name='status',
            field=models.SlugField(default=b'active', max_length=10, choices=[(b'active', b'active'), (b'done', b'done'), (b'archived', b'archived')]),
        ),
    ]
