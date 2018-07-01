# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('word', '0003_auto_20180628_1528'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paraphrase',
            name='example',
            field=models.ManyToManyField(blank=True, null=True, to='word.Example'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='learning_word_set',
            field=models.ForeignKey(blank=True, null=True, related_name='learning_word_set', to='word.WordSet'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='my_words',
            field=models.ManyToManyField(blank=True, null=True, related_name='my_words', to='word.Word'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='task',
            field=models.ManyToManyField(blank=True, null=True, to='word.Word', through='word.Learn'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='word_sets',
            field=models.ManyToManyField(blank=True, null=True, to='word.WordSet'),
        ),
    ]
