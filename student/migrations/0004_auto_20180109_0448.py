# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-09 09:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0003_auto_20180109_0413'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='transcripts',
            new_name='transcript',
        ),
    ]