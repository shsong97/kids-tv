# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-19 00:00
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.utils.timezone

class Migration(migrations.Migration):

    dependencies = [
        ('kid', '0003_auto_20161116_0105'),
    ]

    operations = [
        migrations.AddField(
            model_name='kid',
            name='view_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='kiduser',
            name='birthday',
            field=models.CharField(default=b'2000-01-01', max_length=10),
        ),
        migrations.AlterField(
            model_name='kiduser',
            name='last_login_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
