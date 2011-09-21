# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Paper'
        db.create_table('papers_paper', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.TextField')()),
            ('authors', self.gf('django.db.models.fields.TextField')()),
            ('journal', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('year', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('volume', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('issue', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('pages', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(default='', max_length=1000, blank=True)),
        ))
        db.send_create_signal('papers', ['Paper'])


    def backwards(self, orm):
        
        # Deleting model 'Paper'
        db.delete_table('papers_paper')


    models = {
        'papers.paper': {
            'Meta': {'object_name': 'Paper'},
            'authors': ('django.db.models.fields.TextField', [], {}),
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
