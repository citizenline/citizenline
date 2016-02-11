# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import improvetext.models
import django.contrib.sites.managers


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        ('improvetext', '0003_auto_20160204_0827'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='text',
            managers=[
                ('objects', improvetext.models.TypeManager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='type',
            managers=[
                ('objects', improvetext.models.TypeManager()),
                ('on_site', django.contrib.sites.managers.CurrentSiteManager()),
            ],
        ),
        migrations.AddField(
            model_name='text',
            name='site',
            field=models.ForeignKey(to='sites.Site', default=1),
            preserve_default=False,
        ),
    ]
