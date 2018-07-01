# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('word', '0009_test_complete'),
    ]

    operations = [
        migrations.RenameField(
            model_name='test',
            old_name='word',
            new_name='words',
        ),
    ]
