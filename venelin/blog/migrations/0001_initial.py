# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(unique=True, max_length=255)),
            ],
            options={
                'verbose_name_plural': 'categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255)),
                ('content', ckeditor.fields.RichTextField()),
                ('seo_keywords', models.CharField(blank=True, default='', max_length=128)),
                ('seo_description', models.CharField(blank=True, default='', max_length=256)),
                ('created', models.DateTimeField(db_index=True, auto_now_add=True)),
                ('modified', models.DateTimeField(db_index=True, auto_now=True)),
                ('is_published', models.BooleanField(default=False)),
                ('category', models.ForeignKey(to='blog.Category', on_delete=models.PROTECT)),
            ],
            options={
                'verbose_name_plural': 'entries',
                'ordering': ('-created',),
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='entry',
            unique_together=set([('category', 'slug')]),
        ),
    ]
