# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-10-25 11:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resume', '0010_resume_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='award',
            name='rkey',
            field=models.CharField(default='1', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='experience',
            name='rkey',
            field=models.CharField(default='1', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='language',
            name='rkey',
            field=models.CharField(default='1', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='school',
            name='rkey',
            field=models.CharField(default='1', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='skill',
            name='rkey',
            field=models.CharField(default='1', max_length=20),
            preserve_default=False,
        ),
    ]
