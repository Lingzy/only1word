# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-09-15 08:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oneword', '0002_auto_20170915_1508'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myfavorite',
            name='collect_time',
        ),
    ]