# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bettertexts', '0007_auto_20160323_1913'),
    ]

    operations = [
        migrations.AddField(
            model_name='textcomment',
            name='involved',
            field=models.BooleanField(help_text='Check this box to make more texts better.', default=False, verbose_name='Stay involved'),
        ),
    ]
