# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0019_remove_todo_subscribed_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='order',
            field=models.PositiveIntegerField(default=1, null=True, blank=True),
        ),
    ]
