# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import venelin.gallery.models
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=60)),
                ('slug', models.SlugField(max_length=60, unique=True)),
                ('created', models.DateTimeField(db_index=True, auto_now_add=True)),
                ('modified', models.DateTimeField(db_index=True, auto_now=True)),
            ],
            options={
                'ordering': ['-created', '-pk'],
                'verbose_name_plural': 'galleries',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, blank=True, help_text='Title of the picture', default='')),
                ('image', imagekit.models.fields.ProcessedImageField(upload_to=venelin.gallery.models.upload_picture_to, max_length=255)),
                ('is_album_logo', models.BooleanField(help_text='If this is checked this picture will be the album logo', default=False)),
                ('uploaded', models.DateTimeField(db_index=True, auto_now_add=True)),
                ('modified', models.DateTimeField(db_index=True, auto_now=True)),
                ('gallery', models.ForeignKey(to='gallery.Gallery')),
            ],
            options={
                'ordering': ['-uploaded', '-pk'],
            },
            bases=(models.Model,),
        ),
    ]
