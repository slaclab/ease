# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-21 21:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alert_config_app', '0004_auto_20170620_1117'),
    ]

    operations = [
        migrations.AddField(
            model_name='trigger',
            name='compare',
            field=models.CharField(blank=True, choices=[('==', '=='), ('<=', '<='), ('>=', '>='), ('<', '<'), ('>', '>'), ('!=', '!=')], max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='trigger',
            name='value',
            field=models.FloatField(blank=True, null=True),
        ),
    ]