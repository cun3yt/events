# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-13 15:57
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('details', django.contrib.postgres.fields.jsonb.JSONField(default={})),
            ],
            options={
                'db_table': 'event',
            },
        ),
    ]
