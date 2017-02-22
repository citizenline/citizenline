# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bettertexts', '0008_textcomment_involved'),
    ]

    operations = [
        migrations.AddField(
            model_name='text',
            name='end_date',
            field=models.DateTimeField(verbose_name='date end', null=True),
        ),
        migrations.AlterField(
            model_name='rating',
            name='question',
            field=models.ForeignKey(verbose_name='Question', to='bettertexts.Question'),
        ),
    ]
