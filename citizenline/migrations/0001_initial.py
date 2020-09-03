# Generated by Django 2.2.10 on 2020-05-04 12:39

import citizenline.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('header', models.TextField(blank=True, max_length=20000, verbose_name='header')),
                ('footer', models.TextField(blank=True, max_length=20000, verbose_name='footer')),
                ('site', models.OneToOneField(default=1, editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='sites.Site')),
            ],
            options={
                'verbose_name': 'site profile',
                'verbose_name_plural': 'site profiles',
            },
            managers=[
                ('objects', citizenline.models.SiteProfileManager()),
            ],
        ),
    ]
