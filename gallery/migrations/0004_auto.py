# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding index on 'Picture', fields ['uploaded']
        db.create_index('gallery_picture', ['uploaded'])

        # Adding index on 'Picture', fields ['modified']
        db.create_index('gallery_picture', ['modified'])

        # Adding index on 'Gallery', fields ['modified']
        db.create_index('gallery_gallery', ['modified'])

        # Adding index on 'Gallery', fields ['created']
        db.create_index('gallery_gallery', ['created'])


    def backwards(self, orm):
        # Removing index on 'Gallery', fields ['created']
        db.delete_index('gallery_gallery', ['created'])

        # Removing index on 'Gallery', fields ['modified']
        db.delete_index('gallery_gallery', ['modified'])

        # Removing index on 'Picture', fields ['modified']
        db.delete_index('gallery_picture', ['modified'])

        # Removing index on 'Picture', fields ['uploaded']
        db.delete_index('gallery_picture', ['uploaded'])


    models = {
        'gallery.gallery': {
            'Meta': {'ordering': "['-created', '-pk']", 'object_name': 'Gallery'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '60'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        'gallery.picture': {
            'Meta': {'ordering': "['-uploaded', '-pk']", 'object_name': 'Picture'},
            'gallery': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pictures'", 'to': "orm['gallery.Gallery']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('imagekit.models.fields.ProcessedImageField', [], {'max_length': '255'}),
            'is_album_logo': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'uploaded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['gallery']