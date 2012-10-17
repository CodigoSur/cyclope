# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Series'
        db.delete_table('series_series')


    def backwards(self, orm):
        # Adding model 'Series'
        db.create_table('series_series', (
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('show_author', self.gf('django.db.models.fields.CharField')(default='SITE', max_length=6)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('allow_comments', self.gf('django.db.models.fields.CharField')(default='SITE', max_length=4)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250, db_index=True)),
            ('modification_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, blank=True)),
            ('slug', self.gf('autoslug.fields.AutoSlugField')(max_length=50, unique_with=(), unique=True, populate_from=None, blank=True)),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('series', ['Series'])


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'series.seriescontent': {
            'Meta': {'ordering': "['order']", 'object_name': 'SeriesContent'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'other_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'other_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'series_contents_rt'", 'to': "orm['contenttypes.ContentType']"}),
            'self_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'self_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'series_contents_lt'", 'to': "orm['contenttypes.ContentType']"})
        }
    }

    complete_apps = ['series']