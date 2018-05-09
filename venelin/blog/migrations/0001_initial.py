# -*- coding: utf-8 -*-
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
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('slug', models.SlugField(unique=True, max_length=255, verbose_name='slug')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
                'ordering': ('title',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('slug', models.SlugField(max_length=255, verbose_name='slug')),
                ('content', ckeditor.fields.RichTextField(verbose_name='content')),
                ('seo_keywords', models.CharField(blank=True, default='', max_length=128, verbose_name='keywords')),
                ('seo_description', models.CharField(blank=True, default='', max_length=256, verbose_name='description')),
                ('created', models.DateTimeField(db_index=True, auto_now_add=True, verbose_name='created at')),
                ('modified', models.DateTimeField(db_index=True, auto_now=True, verbose_name='modified at')),
                ('is_published', models.BooleanField(default=False, verbose_name='is published')),
                ('category', models.ForeignKey(to='blog.Category', on_delete=models.PROTECT, related_name='entries', verbose_name='category')),
            ],
            options={
                'verbose_name': 'entry',
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
