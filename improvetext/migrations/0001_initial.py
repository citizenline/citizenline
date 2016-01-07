# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('author', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=200)),
                ('body', models.CharField(max_length=2000)),
                ('notify', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Improvetext',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('slug', models.CharField(max_length=200)),
                ('body', models.CharField(max_length=2000)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
            ],
        ),
        migrations.CreateModel(
            name='Texttype',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='improvetext',
            name='texttype',
            field=models.ForeignKey(to='improvetext.Texttype'),
        ),
        migrations.AddField(
            model_name='comment',
            name='improvetext',
            field=models.ForeignKey(to='improvetext.Improvetext'),
        ),
    ]
