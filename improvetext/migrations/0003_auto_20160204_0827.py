# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_extensions.db.fields
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        ('improvetext', '0002_auto_20160203_1645'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='question',
            options={'verbose_name_plural': 'vragen', 'verbose_name': 'vraag'},
        ),
        migrations.AlterModelOptions(
            name='text',
            options={'verbose_name_plural': 'teksten', 'verbose_name': 'tekst'},
        ),
        migrations.AlterModelOptions(
            name='type',
            options={'verbose_name_plural': 'communicatie soorten', 'verbose_name': 'communicatie soort'},
        ),
        migrations.AddField(
            model_name='type',
            name='site',
            field=models.ForeignKey(to='sites.Site', default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='question',
            name='position',
            field=models.IntegerField(verbose_name='positie'),
        ),
        migrations.AlterField(
            model_name='question',
            name='question',
            field=models.CharField(verbose_name='vraag', max_length=200),
        ),
        migrations.AlterField(
            model_name='text',
            name='body',
            field=ckeditor.fields.RichTextField(verbose_name='tekst', max_length=20000),
        ),
        migrations.AlterField(
            model_name='text',
            name='pub_date',
            field=models.DateTimeField(verbose_name='Publicatie datum', auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='text',
            name='slug',
            field=django_extensions.db.fields.RandomCharField(blank=True, editable=False, unique=True, length=8, verbose_name='slak'),
        ),
        migrations.AlterField(
            model_name='text',
            name='title',
            field=models.CharField(verbose_name='titel', max_length=200),
        ),
        migrations.AlterField(
            model_name='text',
            name='version',
            field=models.PositiveIntegerField(verbose_name='versie', default=0),
        ),
        migrations.AlterField(
            model_name='type',
            name='comment_enabled',
            field=models.BooleanField(verbose_name='reactie plaatsen tonen', default=True),
        ),
        migrations.AlterField(
            model_name='type',
            name='comment_header',
            field=models.CharField(blank=True, verbose_name='reactie plaatsen header', max_length=200),
        ),
        migrations.AlterField(
            model_name='type',
            name='header',
            field=models.CharField(verbose_name='hoofd header', max_length=200),
        ),
        migrations.AlterField(
            model_name='type',
            name='name',
            field=models.CharField(verbose_name='Naam', max_length=200),
        ),
        migrations.AlterField(
            model_name='type',
            name='notification_enabled',
            field=models.BooleanField(verbose_name='notificatie vraag tonen', default=True),
        ),
        migrations.AlterField(
            model_name='type',
            name='rating_enabled',
            field=models.BooleanField(verbose_name='waardering tonen', default=True),
        ),
        migrations.AlterField(
            model_name='type',
            name='rating_header',
            field=models.CharField(blank=True, verbose_name='beoordeling header', max_length=200),
        ),
        migrations.AlterField(
            model_name='type',
            name='response_header',
            field=models.CharField(blank=True, verbose_name='reacties header', max_length=200),
        ),
    ]
