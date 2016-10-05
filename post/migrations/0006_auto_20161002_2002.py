# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-02 20:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0005_auto_20161002_1944'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photo',
            name='post',
        ),
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(default='/static/no-avatar.jpg', upload_to='photos'),
        ),
        migrations.DeleteModel(
            name='Photo',
        ),
    ]
