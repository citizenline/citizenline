# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import ckeditor.fields
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('bettertexts', '0002_auto_20160218_0732'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='question',
            options={'verbose_name': 'question', 'verbose_name_plural': 'questions'},
        ),
        migrations.AlterModelOptions(
            name='text',
            options={'verbose_name': 'text', 'verbose_name_plural': 'texts'},
        ),
        migrations.AlterModelOptions(
            name='type',
            options={'verbose_name': 'communication type', 'verbose_name_plural': 'communication types'},
        ),
        migrations.AlterField(
            model_name='question',
            name='position',
            field=models.IntegerField(verbose_name='position'),
        ),
        migrations.AlterField(
            model_name='question',
            name='question',
            field=models.CharField(verbose_name='question', max_length=200),
        ),
        migrations.AlterField(
            model_name='text',
            name='body',
            field=ckeditor.fields.RichTextField(verbose_name='text', max_length=20000),
        ),
        migrations.AlterField(
            model_name='text',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='date published'),
        ),
        migrations.AlterField(
            model_name='text',
            name='slug',
            field=django_extensions.db.fields.RandomCharField(length=8, blank=True, verbose_name='slug', unique=True, editable=False),
        ),
        migrations.AlterField(
            model_name='text',
            name='title',
            field=models.CharField(verbose_name='title', max_length=200),
        ),
        migrations.AlterField(
            model_name='text',
            name='version',
            field=models.PositiveIntegerField(verbose_name='version', default=0),
        ),
        migrations.AlterField(
            model_name='type',
            name='comment_enabled',
            field=models.BooleanField(verbose_name='comment enabled', default=True),
        ),
        migrations.AlterField(
            model_name='type',
            name='comment_header',
            field=models.CharField(verbose_name='comment header', blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='type',
            name='header',
            field=models.CharField(verbose_name='main header', max_length=200),
        ),
        migrations.AlterField(
            model_name='type',
            name='name',
            field=models.CharField(verbose_name='name', max_length=200),
        ),
        migrations.AlterField(
            model_name='type',
            name='notification_enabled',
            field=models.BooleanField(verbose_name='notification enabled', default=True),
        ),
        migrations.AlterField(
            model_name='type',
            name='rating_enabled',
            field=models.BooleanField(verbose_name='rating enabled', default=True),
        ),
        migrations.AlterField(
            model_name='type',
            name='rating_header',
            field=models.CharField(verbose_name='rating header', blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='type',
            name='response_header',
            field=models.CharField(verbose_name='response header', blank=True, max_length=200),
        ),
    ]
