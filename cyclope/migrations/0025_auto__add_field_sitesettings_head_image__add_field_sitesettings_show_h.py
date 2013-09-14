# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'SiteSettings.head_image'
        db.add_column('cyclope_sitesettings', 'head_image',
                      self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'SiteSettings.show_head_title'
        db.add_column('cyclope_sitesettings', 'show_head_title',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'SiteSettings.body_font'
        db.add_column('cyclope_sitesettings', 'body_font',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=50),
                      keep_default=False)

        # Adding field 'SiteSettings.body_custom_font'
        db.add_column('cyclope_sitesettings', 'body_custom_font',
                      self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'SiteSettings.titles_font'
        db.add_column('cyclope_sitesettings', 'titles_font',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=50),
                      keep_default=False)

        # Adding field 'SiteSettings.titles_custom_font'
        db.add_column('cyclope_sitesettings', 'titles_custom_font',
                      self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'SiteSettings.font_size'
        db.add_column('cyclope_sitesettings', 'font_size',
                      self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=12),
                      keep_default=False)

        # Adding field 'SiteSettings.hide_content_icons'
        db.add_column('cyclope_sitesettings', 'hide_content_icons',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'SiteSettings.head_image'
        db.delete_column('cyclope_sitesettings', 'head_image')

        # Deleting field 'SiteSettings.show_head_title'
        db.delete_column('cyclope_sitesettings', 'show_head_title')

        # Deleting field 'SiteSettings.body_font'
        db.delete_column('cyclope_sitesettings', 'body_font')

        # Deleting field 'SiteSettings.body_custom_font'
        db.delete_column('cyclope_sitesettings', 'body_custom_font')

        # Deleting field 'SiteSettings.titles_font'
        db.delete_column('cyclope_sitesettings', 'titles_font')

        # Deleting field 'SiteSettings.titles_custom_font'
        db.delete_column('cyclope_sitesettings', 'titles_custom_font')

        # Deleting field 'SiteSettings.font_size'
        db.delete_column('cyclope_sitesettings', 'font_size')

        # Deleting field 'SiteSettings.hide_content_icons'
        db.delete_column('cyclope_sitesettings', 'hide_content_icons')


    models = {
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
        'cyclope.author': {
            'Meta': {'ordering': "['name']", 'object_name': 'Author'},
            'content_types': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['contenttypes.ContentType']", 'db_index': 'True', 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('filebrowser.fields.FileBrowseField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250', 'db_index': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'origin': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True', 'blank': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': 'None', 'unique_with': '()', 'blank': 'True'})
        },
        'cyclope.image': {
            'Meta': {'object_name': 'Image'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('filebrowser.fields.FileBrowseField', [], {'max_length': '100'})
        },
        'cyclope.layout': {
            'Meta': {'object_name': 'Layout'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': 'None'}),
            'template': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'cyclope.menu': {
            'Meta': {'object_name': 'Menu'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_menu': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': 'None'})
        },
        'cyclope.menuitem': {
            'Meta': {'object_name': 'MenuItem'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'menu_entries'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}),
            'content_view': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'custom_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'layout': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cyclope.Layout']", 'null': 'True', 'blank': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'menu': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'menu_items'", 'to': "orm['cyclope.Menu']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['cyclope.MenuItem']"}),
            'persistent_layout': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'site_home': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': 'None', 'blank': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'view_options': ('jsonfield.fields.JSONField', [], {'default': "'{}'"})
        },
        'cyclope.regionview': {
            'Meta': {'object_name': 'RegionView'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'region_views'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}),
            'content_view': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'layout': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cyclope.Layout']"}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'view_options': ('jsonfield.fields.JSONField', [], {'default': "'{}'"}),
            'weight': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'})
        },
        'cyclope.relatedcontent': {
            'Meta': {'ordering': "['order']", 'object_name': 'RelatedContent'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'other_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'other_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'related_contents_rt'", 'to': "orm['contenttypes.ContentType']"}),
            'self_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'self_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'related_contents_lt'", 'to': "orm['contenttypes.ContentType']"})
        },
        'cyclope.sitesettings': {
            'Meta': {'object_name': 'SiteSettings'},
            'allow_comments': ('django.db.models.fields.CharField', [], {'default': "'YES'", 'max_length': '4'}),
            'body_custom_font': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'body_font': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'default_layout': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cyclope.Layout']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'enable_abuse_reports': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'enable_comments_notifications': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'enable_follow_buttons': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'enable_ratings': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'enable_share_buttons': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'font_size': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '12'}),
            'global_title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'head_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'hide_content_icons': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keywords': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'moderate_comments': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'newsletter_collection': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['collections.Collection']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'rss_content_types': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['contenttypes.ContentType']", 'symmetrical': 'False'}),
            'show_author': ('django.db.models.fields.CharField', [], {'default': "'AUTHOR'", 'max_length': '6'}),
            'show_head_title': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']", 'unique': 'True'}),
            'social_follow_services': ('jsonfield.fields.JSONField', [], {'default': '\'[["twitter","USERNAME"],["facebook","USERNAME"],["google","USERNAME"],["flickr","USERNAME"],["linkedin","USERNAME"],["vimeo","USERNAME"],["youtube","USERNAME"]]\''}),
            'theme': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'titles_custom_font': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'titles_font': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'})
        },
        'cyclope.source': {
            'Meta': {'object_name': 'Source'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250', 'db_index': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': 'None', 'unique_with': '()'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['cyclope']