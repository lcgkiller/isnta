# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-26 15:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0009_auto_20170626_1606'),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('youtube_id', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('title', models.CharField(blank=True, max_length=80, null=True)),
                ('thumbnails', models.ImageField(upload_to='youtube')),
                ('created_date', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
