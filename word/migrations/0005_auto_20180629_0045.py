# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('word', '0004_auto_20180628_2126'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='task',
            new_name='tasks',
        ),
    ]
