# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('word', '0005_auto_20180629_0045'),
    ]

    operations = [
        migrations.CreateModel(
            name='TodayTask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('date', models.DateField()),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('word', models.ForeignKey(to='word.Word')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='todaytask',
            unique_together=set([('user', 'word', 'date')]),
        ),
    ]
