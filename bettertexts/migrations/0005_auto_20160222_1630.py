# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('bettertexts', '0004_auto_20160218_2018'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='question',
            options={'ordering': ('position',), 'verbose_name': 'question', 'verbose_name_plural': 'questions'},
        ),
        migrations.AlterField(
            model_name='rating',
            name='average',
            field=models.DecimalField(decimal_places=2, default=Decimal('0'), verbose_name='average', max_digits=6),
        ),
        migrations.AlterField(
            model_name='rating',
            name='count',
            field=models.PositiveIntegerField(default=0, verbose_name='count'),
        ),
        migrations.AlterField(
            model_name='rating',
            name='range',
            field=models.PositiveIntegerField(default=10, verbose_name='range'),
        ),
        migrations.AlterField(
            model_name='rating',
            name='total',
            field=models.PositiveIntegerField(default=0, verbose_name='total'),
        ),
        migrations.AlterField(
            model_name='rating',
            name='version',
            field=models.PositiveIntegerField(default=0, verbose_name='version'),
        ),
    ]
