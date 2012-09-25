# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Entry.content'
        db.alter_column('blog_entry', 'content', self.gf('tinymce.models.HTMLField')())


    def backwards(self, orm):
        
        # Changing field 'Entry.content'
        db.alter_column('blog_entry', 'content', self.gf('django.db.models.fields.TextField')())


    models = {
        'blog.category': {
            'Meta': {'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'blog.entry': {
            'Meta': {'ordering': "('-created',)", 'unique_together': "(('category', 'slug'),)", 'object_name': 'Entry'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entries'", 'to': "orm['blog.Category']"}),
            'content': ('tinymce.models.HTMLField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['blog']
