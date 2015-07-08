# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0018_auto_20150706_1553'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='todo',
            name='subscribed_users',
        ),
    ]
