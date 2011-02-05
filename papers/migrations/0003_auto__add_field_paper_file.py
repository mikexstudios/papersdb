# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Paper.file'
        db.add_column('papers_paper', 'file', self.gf('django.db.models.fields.CharField')(default='', max_length=305, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Paper.file'
        db.delete_column('papers_paper', 'file')


    models = {
        'papers.paper': {
            'Meta': {'object_name': 'Paper'},
            'authors': ('django.db.models.fields.TextField', [], {}),
            'file': ('django.db.models.fields.CharField', [], {'max_length': '305', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'journal': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'pages': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'title': ('django.db.models.fields.TextField', [], {}),
            'url': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '1000', 'blank': 'True'}),
            'volume': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'year': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['papers']
