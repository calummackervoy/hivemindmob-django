# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2020-02-15 15:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hive', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='groups', to='content.NameContent'),
        ),
    ]
