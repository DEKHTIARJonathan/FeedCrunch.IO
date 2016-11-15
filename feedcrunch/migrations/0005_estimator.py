# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-15 01:03
from __future__ import unicode_literals

from django.db import migrations, models
import feedcrunch.model_files.models_estimators


class Migration(migrations.Migration):

    dependencies = [
        ('feedcrunch', '0004_auto_20161112_1243'),
    ]

    operations = [
        migrations.CreateModel(
            name='Estimator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified_date', models.DateTimeField(auto_now_add=True)),
                ('object_file', models.FileField(blank=True, default='', editable=False, upload_to=feedcrunch.model_files.models_estimators.get_upload_path_instance)),
                ('description', models.CharField(max_length=256)),
            ],
        ),
    ]
