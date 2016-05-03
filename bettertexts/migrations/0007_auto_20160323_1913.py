# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sites', '0001_initial'),
        ('bettertexts', '0006_auto_20160223_0832'),
    ]

    operations = [
        migrations.CreateModel(
            name='TextComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('object_pk', models.TextField(verbose_name='object ID')),
                ('user_name', models.CharField(max_length=50, verbose_name="user's name", blank=True)),
                ('user_email', models.EmailField(max_length=254, verbose_name="user's email address", blank=True)),
                ('user_url', models.URLField(verbose_name="user's URL", blank=True)),
                ('inform', models.BooleanField(default=False, verbose_name='Keep informed', help_text='Check this box to keep me informed about updates.')),
                ('comment', models.TextField(max_length=3000, verbose_name='comment')),
                ('submit_date', models.DateTimeField(default=None, verbose_name='date/time submitted')),
                ('ip_address', models.GenericIPAddressField(verbose_name='IP address', unpack_ipv4=True, null=True, blank=True)),
                ('is_public', models.BooleanField(default=True, verbose_name='is public', help_text='Uncheck this box to make the comment effectively disappear from the site.')),
                ('is_removed', models.BooleanField(default=False, verbose_name='is removed', help_text='Check this box if the comment is inappropriate. A "This comment has been removed" message will be displayed instead.')),
                ('content_type', models.ForeignKey(verbose_name='content type', related_name='content_type_set_for_textcomment', to='contenttypes.ContentType')),
                ('site', models.ForeignKey(to='sites.Site')),
                ('user', models.ForeignKey(null=True, blank=True, verbose_name='user', related_name='textcomment_comments', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('submit_date',),
                'verbose_name': 'comment',
                'verbose_name_plural': 'comments',
                'permissions': [('can_moderate', 'Can moderate comments')],
            },
        ),
        migrations.RemoveField(
            model_name='comment',
            name='text',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
