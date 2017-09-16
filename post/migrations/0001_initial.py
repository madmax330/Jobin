# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-09 02:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('resume', '0001_initial'),
        ('student', '0001_initial'),
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('opened', models.BooleanField(default=False)),
                ('status', models.CharField(max_length=25)),
                ('cover', models.TextField(blank=True, null=True)),
                ('cover_requested', models.BooleanField(default=False)),
                ('cover_submitted', models.BooleanField(default=False)),
                ('cover_opened', models.BooleanField(default=False)),
                ('post_title', models.CharField(max_length=100)),
                ('student_name', models.CharField(max_length=100)),
                ('resume_notified', models.BooleanField(default=False)),
                ('saved', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('wage', models.IntegerField(blank=True, null=True)),
                ('wage_interval', models.CharField(max_length=20)),
                ('openings', models.IntegerField(null=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('deadline', models.DateField()),
                ('description', models.TextField()),
                ('requirements', models.TextField()),
                ('schools', models.CharField(default='ALL', max_length=200, null=True)),
                ('programs', models.CharField(default='ALL', max_length=200, null=True)),
                ('type', models.CharField(max_length=100, null=True)),
                ('status', models.CharField(default='open', max_length=50, null=True)),
                ('supplied_by_jobin', models.BooleanField(default=True)),
                ('notified', models.BooleanField(default=False)),
                ('new_apps', models.BooleanField(default=False)),
                ('cover_instructions', models.TextField(blank=True, null=True)),
                ('is_startup_post', models.BooleanField(default=False)),
                ('views', models.IntegerField(default=0)),
                ('date_posted', models.DateField(auto_now_add=True)),
                ('location', models.CharField(max_length=200)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='company.Company')),
            ],
        ),
        migrations.AddField(
            model_name='application',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='post.Post'),
        ),
        migrations.AddField(
            model_name='application',
            name='resume',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='resume.Resume'),
        ),
        migrations.AddField(
            model_name='application',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='student.Student'),
        ),
    ]