# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-14 14:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0003_remove_event_details'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_id',
            field=models.TextField(db_index=True),
        ),
    ]