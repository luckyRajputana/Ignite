# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2019-10-09 19:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0002_auto_20191010_0043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assembly',
            name='assembly_line_no',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='assembly',
            name='bin_id',
            field=models.IntegerField(),
        ),
    ]
