# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-02 23:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0011_post_visibility'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='title',
            field=models.CharField(blank=True, max_length=60),
        ),
    ]
