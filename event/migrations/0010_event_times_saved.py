# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-24 10:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0009_auto_20170123_1946'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='times_saved',
            field=models.IntegerField(default=0),
        ),
    ]
