# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-12 03:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='content',
            field=models.TextField(blank=True, null=True),
        ),
    ]
