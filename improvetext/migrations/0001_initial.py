# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from decimal import Decimal
import model_utils.fields
import ckeditor.fields
import django.utils.timezone
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('version', models.PositiveIntegerField(default=0)),
                ('author', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=200)),
                ('body', models.CharField(max_length=2000)),
                ('notify', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('question', models.CharField(max_length=200)),
                ('position', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('count', models.PositiveIntegerField(default=0)),
                ('total', models.PositiveIntegerField(default=0)),
                ('average', models.DecimalField(decimal_places=3, max_digits=6, default=Decimal('0'))),
                ('version', models.PositiveIntegerField(default=0)),
                ('question', models.ForeignKey(to='improvetext.Question')),
            ],
        ),
        migrations.CreateModel(
            name='Text',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('slug', django_extensions.db.fields.RandomCharField(unique=True, blank=True, editable=False, length=8)),
                ('body', ckeditor.fields.RichTextField(max_length=2000)),
                ('version', models.PositiveIntegerField(default=0)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('header', models.CharField(max_length=200)),
                ('rating_header', models.CharField(max_length=200)),
                ('comment_header', models.CharField(max_length=200)),
                ('rating_enabled', models.BooleanField(default=True)),
                ('comment_enabled', models.BooleanField(default=True)),
                ('notification_enabled', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserRating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('created', model_utils.fields.AutoCreatedField(verbose_name='created', editable=False, default=django.utils.timezone.now)),
                ('modified', model_utils.fields.AutoLastModifiedField(verbose_name='modified', editable=False, default=django.utils.timezone.now)),
                ('user', models.CharField(max_length=200)),
                ('ip', models.GenericIPAddressField(blank=True, null=True)),
                ('score', models.PositiveSmallIntegerField()),
                ('rating', models.ForeignKey(related_name='user_ratings', to='improvetext.Rating')),
            ],
        ),
        migrations.AddField(
            model_name='text',
            name='type',
            field=models.ForeignKey(to='improvetext.Type'),
        ),
        migrations.AddField(
            model_name='rating',
            name='text',
            field=models.ForeignKey(to='improvetext.Text'),
        ),
        migrations.AddField(
            model_name='question',
            name='type',
            field=models.ForeignKey(to='improvetext.Type'),
        ),
        migrations.AddField(
            model_name='comment',
            name='text',
            field=models.ForeignKey(to='improvetext.Text'),
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
