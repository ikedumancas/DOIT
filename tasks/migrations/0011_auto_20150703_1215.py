# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0010_auto_20150703_1203'),
    ]

    operations = [
        migrations.RenameField(
            model_name='todo',
            old_name='todo',
            new_name='title',
        ),
    ]
