# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-27 04:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import utils.fields.custom_imagefield


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0013_auto_20170627_1346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='photo',
            field=utils.fields.custom_imagefield.CustomImageField(blank=True, upload_to='post'),
        ),
        migrations.AlterField(
            model_name='post',
            name='video',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='post.Video'),
        ),
    ]
