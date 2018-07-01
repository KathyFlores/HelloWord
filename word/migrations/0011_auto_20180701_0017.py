# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('word', '0010_auto_20180630_2354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='complete',
            field=models.IntegerField(default=0),
        ),
    ]
