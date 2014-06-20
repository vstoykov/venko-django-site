# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Picture.thumb'
        db.delete_column('gallery_picture', 'thumb')


        # Changing field 'Picture.image'
        db.alter_column('gallery_picture', 'image', self.gf('imagekit.models.fields.ProcessedImageField')(max_length=255))

    def backwards(self, orm):
        # Adding field 'Picture.thumb'
        db.add_column('gallery_picture', 'thumb',
                      self.gf('django.db.models.fields.files.ImageField')(max_length=255, null=True, blank=True),
                      keep_default=False)


        # Changing field 'Picture.image'
        db.alter_column('gallery_picture', 'image', self.gf('django.db.models.fields.files.ImageField')(max_length=255))

    models = {
        'gallery.gallery': {
            'Meta': {'ordering': "['-created', '-pk']", 'object_name': 'Gallery'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '60'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        'gallery.picture': {
            'Meta': {'ordering': "['-uploaded', '-pk']", 'object_name': 'Picture'},
            'gallery': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pictures'", 'to': "orm['gallery.Gallery']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('imagekit.models.fields.ProcessedImageField', [], {'max_length': '255'}),
            'is_album_logo': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'uploaded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['gallery']