# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-26 08:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0007_auto_20161124_0917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='address',
            field=models.CharField(default='address', max_length=256),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='company',
            name='city',
            field=models.CharField(default='city', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='company',
            name='country',
            field=models.CharField(default='country', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='company',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='points',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='company',
            name='state',
            field=models.CharField(default='state', max_length=25),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='company',
            name='zipcode',
            field=models.CharField(default='code', max_length=20),
            preserve_default=False,
        ),
    ]
