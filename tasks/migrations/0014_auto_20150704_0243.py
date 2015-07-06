# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0013_auto_20150704_0236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='subscribed_users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
