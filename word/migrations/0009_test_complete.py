# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('word', '0008_test'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='complete',
            field=models.BooleanField(default=False),
        ),
    ]
