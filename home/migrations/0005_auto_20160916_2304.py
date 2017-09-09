# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-09-16 23:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_auto_20160916_2302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='company.Company'),
        ),
        migrations.AlterField(
            model_name='message',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='student.Student'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='company.Company'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='student.Student'),
        ),
    ]
