# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-11-24 09:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_jobinblockedemail_jobinrequestedemail'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobinInvalidUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='user', max_length=100)),
                ('user', models.CharField(max_length=100, null=True)),
                ('category', models.CharField(max_length=100)),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
    ]
