# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-08 11:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reg', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='register',
            name='dob',
            field=models.CharField(max_length=10),
        ),
    ]
