# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-04 16:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0002_auto_20171102_1802'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='billed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='entry',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created at'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='hours',
            field=models.TimeField(blank=True, help_text='You can also enter minutes.'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='message',
            field=models.CharField(help_text='Brief description of work done.<br>Add SVN revision or issue number if available.', max_length=255),
        ),
        migrations.AlterField(
            model_name='entry',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Updated at'),
        ),
    ]