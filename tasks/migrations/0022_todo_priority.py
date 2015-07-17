# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0021_auto_20150717_2244'),
    ]

    operations = [
        migrations.AddField(
            model_name='todo',
            name='priority',
            field=models.CharField(default=b'normal', max_length=10, choices=[(b'critical', b'Critical'), (b'high', b'High'), (b'normal', b'Normal'), (b'low', b'Low'), (b'minor', b'Minor')]),
        ),
    ]
