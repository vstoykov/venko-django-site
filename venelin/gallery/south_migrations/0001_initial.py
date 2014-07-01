# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Gallery'
        db.create_table('gallery_gallery', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=60, db_index=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('gallery', ['Gallery'])

        # Adding model 'Picture'
        db.create_table('gallery_picture', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('gallery', self.gf('django.db.models.fields.related.ForeignKey')(related_name='pictures', to=orm['gallery.Gallery'])),
            ('title', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=255)),
            ('thumb', self.gf('django.db.models.fields.files.ImageField')(max_length=255, null=True, blank=True)),
            ('uploaded', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('gallery', ['Picture'])


    def backwards(self, orm):
        
        # Deleting model 'Gallery'
        db.delete_table('gallery_gallery')

        # Deleting model 'Picture'
        db.delete_table('gallery_picture')


    models = {
        'gallery.gallery': {
            'Meta': {'object_name': 'Gallery'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '60', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        'gallery.picture': {
            'Meta': {'object_name': 'Picture'},
            'gallery': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pictures'", 'to': "orm['gallery.Gallery']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'thumb': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'uploaded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['gallery']
