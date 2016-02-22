# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bettertexts', '0003_auto_20160218_0740'),
    ]

    operations = [
        migrations.AddField(
            model_name='rating',
            name='range',
            field=models.PositiveIntegerField(default=10),
        ),
        migrations.AlterField(
            model_name='userrating',
            name='rating',
            field=models.ForeignKey(to='bettertexts.Rating', related_name='user_ratings', editable=False),
        ),
    ]
