# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-20 05:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0005_comment_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='tags',
            field=models.ManyToManyField(to='post.Tag'),
        ),
    ]
