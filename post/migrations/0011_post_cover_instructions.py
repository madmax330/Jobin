# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-10-14 14:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0010_auto_20161005_0948'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='cover_instructions',
            field=models.TextField(blank=True, null=True),
        ),
    ]
