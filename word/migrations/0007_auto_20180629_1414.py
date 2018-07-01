# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('word', '0006_auto_20180629_1310'),
    ]

    operations = [
        migrations.RenameField(
            model_name='paraphrase',
            old_name='example',
            new_name='examples',
        ),
    ]
