# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-07 17:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boxer', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='picture',
            old_name='user',
            new_name='owner',
        ),
    ]
