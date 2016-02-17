# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import ckeditor.fields
import django.utils.timezone
import model_utils.fields
import django.contrib.sites.managers
from decimal import Decimal
import django_extensions.db.fields
import bettertexts.models


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('version', models.PositiveIntegerField(default=0)),
                ('author', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=200)),
                ('body', models.CharField(max_length=20000)),
                ('notify', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question', models.CharField(verbose_name='vraag', max_length=200)),
                ('position', models.IntegerField(verbose_name='positie')),
            ],
            options={
                'verbose_name': 'vraag',
                'verbose_name_plural': 'vragen',
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('count', models.PositiveIntegerField(default=0)),
                ('total', models.PositiveIntegerField(default=0)),
                ('average', models.DecimalField(decimal_places=3, default=Decimal('0'), max_digits=6)),
                ('version', models.PositiveIntegerField(default=0)),
                ('question', models.ForeignKey(to='bettertexts.Question')),
            ],
        ),
        migrations.CreateModel(
            name='Text',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(verbose_name='titel', max_length=200)),
                ('slug', django_extensions.db.fields.RandomCharField(unique=True, blank=True, verbose_name='slak', editable=False, length=8)),
                ('body', ckeditor.fields.RichTextField(verbose_name='tekst', max_length=20000)),
                ('version', models.PositiveIntegerField(verbose_name='versie', default=0)),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Publicatie datum')),
                ('site', models.ForeignKey(to='sites.Site', editable=False, default=1)),
            ],
            options={
                'verbose_name': 'tekst',
                'verbose_name_plural': 'teksten',
            },
            managers=[
                ('objects', bettertexts.models.TypeManager()),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(verbose_name='Naam', max_length=200)),
                ('header', models.CharField(verbose_name='hoofd header', max_length=200)),
                ('rating_header', models.CharField(blank=True, verbose_name='beoordeling header', max_length=200)),
                ('comment_header', models.CharField(blank=True, verbose_name='reactie plaatsen header', max_length=200)),
                ('response_header', models.CharField(blank=True, verbose_name='reacties header', max_length=200)),
                ('rating_enabled', models.BooleanField(verbose_name='waardering tonen', default=True)),
                ('comment_enabled', models.BooleanField(verbose_name='reactie plaatsen tonen', default=True)),
                ('notification_enabled', models.BooleanField(verbose_name='notificatie vraag tonen', default=True)),
                ('site', models.ForeignKey(to='sites.Site')),
            ],
            options={
                'verbose_name': 'communicatie soort',
                'verbose_name_plural': 'communicatie soorten',
            },
            managers=[
                ('objects', bettertexts.models.TypeManager()),
                ('on_site', django.contrib.sites.managers.CurrentSiteManager()),
            ],
        ),
        migrations.CreateModel(
            name='UserRating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(verbose_name='created', editable=False, default=django.utils.timezone.now)),
                ('modified', model_utils.fields.AutoLastModifiedField(verbose_name='modified', editable=False, default=django.utils.timezone.now)),
                ('user', models.CharField(max_length=200)),
                ('ip', models.GenericIPAddressField(null=True, blank=True)),
                ('score', models.PositiveSmallIntegerField()),
                ('rating', models.ForeignKey(related_name='user_ratings', to='bettertexts.Rating')),
            ],
        ),
        migrations.AddField(
            model_name='text',
            name='type',
            field=models.ForeignKey(to='bettertexts.Type'),
        ),
        migrations.AddField(
            model_name='rating',
            name='text',
            field=models.ForeignKey(to='bettertexts.Text'),
        ),
        migrations.AddField(
            model_name='question',
            name='type',
            field=models.ForeignKey(to='bettertexts.Type'),
        ),
        migrations.AddField(
            model_name='comment',
            name='text',
            field=models.ForeignKey(to='bettertexts.Text'),
        ),
        migrations.AlterUniqueTogether(
            name='userrating',
            unique_together=set([('user', 'rating')]),
        ),
        migrations.AlterUniqueTogether(
            name='rating',
            unique_together=set([('text', 'version', 'question')]),
        ),
    ]
