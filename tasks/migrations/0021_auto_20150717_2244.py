# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0020_auto_20150708_1432'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todolist',
            name='creator',
            field=models.ForeignKey(related_name='created_list', default=1, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='todolist',
            name='users',
            field=models.ManyToManyField(related_name='lists', to=settings.AUTH_USER_MODEL),
        ),
    ]
