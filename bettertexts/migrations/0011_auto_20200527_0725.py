# Generated by Django 2.2.3 on 2020-05-27 05:25

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bettertexts', '0010_auto_20171130_0705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='text',
            name='intro',
            field=ckeditor.fields.RichTextField(blank=True, default='', max_length=20000, verbose_name='intro'),
            preserve_default=False,
        ),
    ]
