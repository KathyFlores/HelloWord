# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('word', '0011_auto_20180701_0017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='learning_word_set',
            field=models.ForeignKey(blank=True, null=True, related_name='learning_word_set', on_delete=django.db.models.deletion.SET_NULL, to='word.WordSet'),
        ),
    ]
