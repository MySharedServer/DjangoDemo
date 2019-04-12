# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-11 00:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aynalize', '0002_auto_20190410_1317'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='functioninfo',
            options={'ordering': ['fileName'], 'verbose_name': 'Function detail', 'verbose_name_plural': 'Function detail'},
        ),
        migrations.RenameField(
            model_name='functioninfo',
            old_name='func_body',
            new_name='body',
        ),
        migrations.RenameField(
            model_name='functioninfo',
            old_name='file_name',
            new_name='fileName',
        ),
        migrations.RenameField(
            model_name='functioninfo',
            old_name='func_line',
            new_name='line',
        ),
        migrations.RenameField(
            model_name='functioninfo',
            old_name='func_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='functioninfo',
            old_name='func_param',
            new_name='params',
        ),
        migrations.AlterField(
            model_name='functioninfo',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
