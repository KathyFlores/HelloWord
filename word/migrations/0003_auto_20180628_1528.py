# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('word', '0002_auto_20180628_0007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paraphrase',
            name='example',
            field=models.ManyToManyField(null=True, to='word.Example'),
        ),
    ]
