# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tasks', '0012_todolist_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='todolist',
            name='creator',
            field=models.ForeignKey(related_name='created_by', default=1, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='todo',
            name='subscribed_users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='todolist',
            name='users',
            field=models.ManyToManyField(related_name='can_modify_users', to=settings.AUTH_USER_MODEL),
        ),
    ]
