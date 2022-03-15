# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-14 09:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_create_homepage'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='company_logo',
            field=models.ImageField(blank=True, upload_to='uploads/home/logo/'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='enable_footer',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='homepage',
            name='footer_subtitle',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='homepage',
            name='footer_title',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='homepage',
            name='home_tagline',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
