# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bettertexts', '0005_auto_20160222_1630'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rating',
            options={'verbose_name': 'rating', 'verbose_name_plural': 'ratings'},
        ),
    ]
