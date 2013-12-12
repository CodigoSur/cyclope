# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Newsletter.regions'
        db.add_column('newsletter_newsletter', 'regions',
                      self.gf('django.db.models.fields.CharField')(default='c', max_length=4),
                      keep_default=False)

        # Adding field 'Newsletter.n_contents_top'
        db.add_column('newsletter_newsletter', 'n_contents_top',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Newsletter.n_contents_center'
        db.add_column('newsletter_newsletter', 'n_contents_center',
                      self.gf('django.db.models.fields.IntegerField')(default=10),
                      keep_default=False)

        # Adding field 'Newsletter.n_contents_lateral'
        db.add_column('newsletter_newsletter', 'n_contents_lateral',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Newsletter.head_image'
        db.add_column('newsletter_newsletter', 'head_image',
                      self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Newsletter.show_title'
        db.add_column('newsletter_newsletter', 'show_title',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'Newsletter.list_admin'
        db.add_column('newsletter_newsletter', 'list_admin',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True),
                      keep_default=False)


        # Changing field 'Newsletter.recipients'
        db.alter_column('newsletter_newsletter', 'recipients', self.gf('django.db.models.fields.CharField')(max_length=255))

    def backwards(self, orm):
        # Deleting field 'Newsletter.regions'
        db.delete_column('newsletter_newsletter', 'regions')

        # Deleting field 'Newsletter.n_contents_top'
        db.delete_column('newsletter_newsletter', 'n_contents_top')

        # Deleting field 'Newsletter.n_contents_center'
        db.delete_column('newsletter_newsletter', 'n_contents_center')

        # Deleting field 'Newsletter.n_contents_lateral'
        db.delete_column('newsletter_newsletter', 'n_contents_lateral')

        # Deleting field 'Newsletter.head_image'
        db.delete_column('newsletter_newsletter', 'head_image')

        # Deleting field 'Newsletter.show_title'
        db.delete_column('newsletter_newsletter', 'show_title')

        # Deleting field 'Newsletter.list_admin'
        db.delete_column('newsletter_newsletter', 'list_admin')


        # Changing field 'Newsletter.recipients'
        db.alter_column('newsletter_newsletter', 'recipients', self.gf('django.db.models.fields.TextField')())

    models = {
        'collections.category': {
            'Meta': {'unique_together': "(('collection', 'name'),)", 'object_name': 'Category'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'categories'", 'to': "orm['collections.Collection']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('filebrowser.fields.FileBrowseField', [], {'max_length': '250', 'blank': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['collections.Category']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': 'None', 'unique_with': '()', 'blank': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'collections.collection': {
            'Meta': {'object_name': 'Collection'},
            'content_types': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['contenttypes.ContentType']", 'db_index': 'True', 'symmetrical': 'False'}),
            'default_list_view': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('filebrowser.fields.FileBrowseField', [], {'max_length': '250', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'navigation_root': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': 'None', 'blank': 'True'}),
            'view_options': ('jsonfield.fields.JSONField', [], {'default': "'{}'"}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'cyclope.layout': {
            'Meta': {'object_name': 'Layout'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': 'None'}),
            'template': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'newsletter.newsletter': {
            'Meta': {'object_name': 'Newsletter'},
            'content_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['collections.Category']"}),
            'head_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'header': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_sent_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'layout': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cyclope.Layout']"}),
            'list_admin': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'n_contents_center': ('django.db.models.fields.IntegerField', [], {'default': '10'}),
            'n_contents_lateral': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'n_contents_top': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'}),
            'recipients': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'regions': ('django.db.models.fields.CharField', [], {'default': "'c'", 'max_length': '4'}),
            'sender': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'sender_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '40', 'blank': 'True'}),
            'show_ToC': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'show_title': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': 'None'}),
            'test_recipients': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'view': ('django.db.models.fields.CharField', [], {'default': "'default'", 'max_length': '255'})
        }
    }

    complete_apps = ['newsletter']