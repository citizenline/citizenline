# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('improvetext', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='type',
            options={'verbose_name': 'improvetext type', 'verbose_name_plural': 'improvetext types'},
        ),
        migrations.AddField(
            model_name='type',
            name='response_header',
            field=models.CharField(verbose_name='response header', max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='body',
            field=models.CharField(max_length=20000),
        ),
        migrations.AlterField(
            model_name='text',
            name='body',
            field=ckeditor.fields.RichTextField(max_length=20000),
        ),
        migrations.AlterField(
            model_name='type',
            name='comment_enabled',
            field=models.BooleanField(default=True, verbose_name='comment enabled'),
        ),
        migrations.AlterField(
            model_name='type',
            name='comment_header',
            field=models.CharField(verbose_name='comment header', max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='type',
            name='notification_enabled',
            field=models.BooleanField(default=True, verbose_name='notification enabled'),
        ),
        migrations.AlterField(
            model_name='type',
            name='rating_enabled',
            field=models.BooleanField(default=True, verbose_name='rating enabled'),
        ),
        migrations.AlterField(
            model_name='type',
            name='rating_header',
            field=models.CharField(verbose_name='rating header', max_length=200, blank=True),
        ),
    ]
