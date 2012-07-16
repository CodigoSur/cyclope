# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Collection.view_options'
        db.add_column('collections_collection', 'view_options', self.gf('jsonfield.fields.JSONField')(default='{}'), keep_default=False)

        # Changing field 'Collection.visible'
        db.alter_column('collections_collection', 'visible', self.gf('django.db.models.fields.BooleanField')(blank=True))

        # Changing field 'Collection.navigation_root'
        db.alter_column('collections_collection', 'navigation_root', self.gf('django.db.models.fields.BooleanField')(blank=True))

        # Changing field 'Collection.name'
        db.alter_column('collections_collection', 'name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100))

        # Changing field 'Category.name'
        db.alter_column('collections_category', 'name', self.gf('django.db.models.fields.CharField')(max_length=100))

        # Adding unique constraint on 'Category', fields ['slug']
        db.create_unique('collections_category', ['slug'])

        # Changing field 'Category.active'
        db.alter_column('collections_category', 'active', self.gf('django.db.models.fields.BooleanField')(blank=True))


    def backwards(self, orm):
        
        # Deleting field 'Collection.view_options'
        db.delete_column('collections_collection', 'view_options')

        # Changing field 'Collection.visible'
        db.alter_column('collections_collection', 'visible', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'Collection.navigation_root'
        db.alter_column('collections_collection', 'navigation_root', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'Collection.name'
        db.alter_column('collections_collection', 'name', self.gf('django.db.models.fields.CharField')(max_length=50, unique=True))

        # Changing field 'Category.name'
        db.alter_column('collections_category', 'name', self.gf('django.db.models.fields.CharField')(max_length=50))

        # Removing unique constraint on 'Category', fields ['slug']
        db.delete_unique('collections_category', ['slug'])

        # Changing field 'Category.active'
        db.alter_column('collections_category', 'active', self.gf('django.db.models.fields.BooleanField')())


    models = {
        'collections.categorization': {
            'Meta': {'object_name': 'Categorization'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'categorizations'", 'to': "orm['collections.Category']"}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'collections.category': {
            'Meta': {'unique_together': "(('collection', 'name'),)", 'object_name': 'Category'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True', 'blank': 'True'}),
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'categories'", 'to': "orm['collections.Collection']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('filebrowser.fields.FileBrowseField', [], {'max_length': '250', 'blank': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['collections.Category']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': 'None', 'unique_with': '()', 'db_index': 'True'}),
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
            'navigation_root': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': 'None', 'db_index': 'True'}),
            'view_options': ('jsonfield.fields.JSONField', [], {'default': "'{}'"}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['collections']
