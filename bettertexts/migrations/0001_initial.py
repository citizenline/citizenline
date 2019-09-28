# Generated by Django 2.2.3 on 2019-09-26 19:42

import bettertexts.models
import ckeditor.fields
from decimal import Decimal
from django.conf import settings
import django.contrib.sites.managers
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_extensions.db.fields
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
        ('sites', '0002_alter_domain_unique'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=200, verbose_name='question')),
                ('position', models.IntegerField(verbose_name='position')),
            ],
            options={
                'verbose_name': 'question',
                'verbose_name_plural': 'questions',
                'ordering': ('position',),
            },
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('header', models.CharField(max_length=200, verbose_name='main header')),
                ('rating_header', models.CharField(blank=True, max_length=200, verbose_name='rating header')),
                ('comment_header', models.CharField(blank=True, max_length=200, verbose_name='comment header')),
                ('response_header', models.CharField(blank=True, max_length=200, verbose_name='response header')),
                ('rating_enabled', models.BooleanField(default=True, verbose_name='rating enabled')),
                ('comment_enabled', models.BooleanField(default=True, verbose_name='comment enabled')),
                ('notification_enabled', models.BooleanField(default=True, verbose_name='notification enabled')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sites.Site')),
            ],
            options={
                'verbose_name': 'communication type',
                'verbose_name_plural': 'communication types',
            },
            managers=[
                ('objects', bettertexts.models.TypeManager()),
                ('on_site', django.contrib.sites.managers.CurrentSiteManager()),
            ],
        ),
        migrations.CreateModel(
            name='TextComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_pk', models.TextField(verbose_name='object ID')),
                ('user_name', models.CharField(blank=True, max_length=50, verbose_name="user's name")),
                ('user_email', models.EmailField(blank=True, max_length=254, verbose_name="user's email address")),
                ('user_url', models.URLField(blank=True, verbose_name="user's URL")),
                ('inform', models.BooleanField(default=False, help_text='Check this box to keep me informed about updates.', verbose_name='Keep informed')),
                ('involved', models.BooleanField(default=False, help_text='Check this box to make more texts better.', verbose_name='Stay involved')),
                ('comment', models.TextField(max_length=3000, verbose_name='comment')),
                ('submit_date', models.DateTimeField(default=None, verbose_name='date/time submitted')),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True, unpack_ipv4=True, verbose_name='IP address')),
                ('is_public', models.BooleanField(default=True, help_text='Uncheck this box to make the comment effectively disappear from the site.', verbose_name='is public')),
                ('is_removed', models.BooleanField(default=False, help_text='Check this box if the comment is inappropriate. A "This comment has been removed" message will be displayed instead.', verbose_name='is removed')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='content_type_set_for_textcomment', to='contenttypes.ContentType', verbose_name='content type')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sites.Site')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='textcomment_comments', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'comment',
                'verbose_name_plural': 'comments',
                'ordering': ('submit_date',),
                'permissions': [('can_moderate', 'Can moderate comments')],
            },
        ),
        migrations.CreateModel(
            name='Text',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='title')),
                ('slug', django_extensions.db.fields.RandomCharField(blank=True, editable=False, length=8, unique=True, verbose_name='slug')),
                ('intro', ckeditor.fields.RichTextField(blank=True, max_length=20000, verbose_name='intro')),
                ('body', ckeditor.fields.RichTextField(max_length=20000, verbose_name='text')),
                ('version', models.PositiveIntegerField(default=0, verbose_name='version')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='date published')),
                ('end_date', models.DateTimeField(blank=True, null=True, verbose_name='date end')),
                ('site', models.ForeignKey(default=1, editable=False, on_delete=django.db.models.deletion.CASCADE, to='sites.Site')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bettertexts.Type')),
            ],
            options={
                'verbose_name': 'text',
                'verbose_name_plural': 'texts',
            },
            managers=[
                ('objects', bettertexts.models.TypeManager()),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.PositiveIntegerField(default=0, verbose_name='version')),
                ('range', models.PositiveIntegerField(default=10, verbose_name='range')),
                ('count', models.PositiveIntegerField(default=0, verbose_name='count')),
                ('total', models.PositiveIntegerField(default=0, verbose_name='total')),
                ('average', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=6, verbose_name='average')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bettertexts.Question', verbose_name='Question')),
                ('text', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bettertexts.Text')),
            ],
            options={
                'verbose_name': 'rating',
                'verbose_name_plural': 'ratings',
                'unique_together': {('text', 'version', 'question')},
            },
        ),
        migrations.AddField(
            model_name='question',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bettertexts.Type'),
        ),
        migrations.CreateModel(
            name='UserRating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('user', models.CharField(max_length=200)),
                ('ip', models.GenericIPAddressField(blank=True, null=True)),
                ('score', models.PositiveSmallIntegerField()),
                ('rating', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='user_ratings', to='bettertexts.Rating')),
            ],
            options={
                'unique_together': {('user', 'rating')},
            },
        ),
    ]
