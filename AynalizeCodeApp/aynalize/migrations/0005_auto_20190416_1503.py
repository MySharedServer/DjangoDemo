# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-16 07:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aynalize', '0004_aynalizestatus'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AynalizeStatus',
            new_name='AnalysisStatus',
        ),
        migrations.AlterModelOptions(
            name='analysisstatus',
            options={'verbose_name': 'analysis status', 'verbose_name_plural': 'analysis status'},
        ),
    ]
