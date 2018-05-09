# -*- coding: utf-8 -*-
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
                ('title', models.CharField(max_length=60, verbose_name='title')),
                ('slug', models.SlugField(max_length=60, unique=True, verbose_name='slug')),
                ('created', models.DateTimeField(db_index=True, auto_now_add=True, verbose_name='created at')),
                ('modified', models.DateTimeField(db_index=True, auto_now=True, verbose_name='modified at')),
            ],
            options={
                'ordering': ('-created', '-pk'),
                'verbose_name': 'gallery',
                'verbose_name_plural': 'galleries',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, blank=True, help_text='Title of the picture', default='', verbose_name='title')),
                ('image', imagekit.models.fields.ProcessedImageField(upload_to=venelin.gallery.models.upload_picture_to, max_length=255, verbose_name='image')),
                ('is_album_logo', models.BooleanField(help_text='If this is checked this picture will be the album logo', default=False, verbose_name='is album logo')),
                ('uploaded', models.DateTimeField(db_index=True, auto_now_add=True, verbose_name='uploaded at')),
                ('modified', models.DateTimeField(db_index=True, auto_now=True, verbose_name='modified at')),
                ('gallery', models.ForeignKey(to='gallery.Gallery', on_delete=models.CASCADE, related_name='pictures', verbose_name='gallery')),
            ],
            options={
                'ordering': ('-uploaded', '-pk'),
                'verbose_name': 'picture',
                'verbose_name_plural': 'pictures'
            },
            bases=(models.Model,),
        ),
    ]
