# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('bettertexts', '0009_auto_20170221_0724'),
    ]

    operations = [
        migrations.AddField(
            model_name='text',
            name='intro',
            field=ckeditor.fields.RichTextField(max_length=20000, null=True, verbose_name='intro'),
        ),
        migrations.AlterField(
            model_name='text',
            name='end_date',
            field=models.DateTimeField(null=True, verbose_name='date end', blank=True),
        ),
    ]
