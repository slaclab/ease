# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-14 17:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alert_config_app', '0006_post'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Post',
            new_name='PVname',
        ),
    ]
