# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('word', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Example',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('sentence', models.CharField(max_length=500)),
                ('translation', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Paraphrase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('meaning', models.CharField(max_length=50)),
                ('example', models.ManyToManyField(to='word.Example')),
            ],
        ),
        migrations.RemoveField(
            model_name='word',
            name='meaning',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='learning_word_set',
            field=models.ForeignKey(default=1, related_name='learning_word_set', to='word.WordSet'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='my_words',
            field=models.ManyToManyField(related_name='my_words', to='word.Word'),
        ),
        migrations.AddField(
            model_name='paraphrase',
            name='word',
            field=models.ForeignKey(to='word.Word'),
        ),
    ]
