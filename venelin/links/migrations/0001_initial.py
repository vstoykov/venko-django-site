# -*- coding: utf-8 -*-
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('title', models.CharField(verbose_name='title', db_index=True, max_length=255)),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('title', models.CharField(verbose_name='title', max_length=255)),
                ('url', models.CharField(verbose_name='URL', max_length=255)),
                ('category', models.ForeignKey(to='links.Category', related_name='links', verbose_name='category', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'link',
                'verbose_name_plural': 'links',
                'ordering': ('category',),
            },
        ),
    ]
