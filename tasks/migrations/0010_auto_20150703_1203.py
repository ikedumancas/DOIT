# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tasks', '0009_auto_20150703_1143'),
    ]

    operations = [
        migrations.AddField(
            model_name='todo',
            name='subscribed_users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='todo',
            name='slug',
            field=models.SlugField(max_length=10, null=True, blank=True),
        ),
    ]
