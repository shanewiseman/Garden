# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-12 23:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('GardenServer', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='device',
            name='password',
        ),
    ]