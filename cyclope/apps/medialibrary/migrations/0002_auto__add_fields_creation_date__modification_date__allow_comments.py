# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'RegularFile.creation_date'
        db.add_column('medialibrary_regularfile', 'creation_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now(), auto_now_add=True, blank=True), keep_default=False)

        # Adding field 'RegularFile.modification_date'
        db.add_column('medialibrary_regularfile', 'modification_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now(), auto_now=True, blank=True), keep_default=False)

        # Adding field 'RegularFile.allow_comments'
        db.add_column('medialibrary_regularfile', 'allow_comments', self.gf('django.db.models.fields.CharField')(default='SITE', max_length=4), keep_default=False)

        # Adding field 'MovieClip.creation_date'
        db.add_column('medialibrary_movieclip', 'creation_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now(), auto_now_add=True, blank=True), keep_default=False)

        # Adding field 'MovieClip.modification_date'
        db.add_column('medialibrary_movieclip', 'modification_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now(), auto_now=True, blank=True), keep_default=False)

        # Adding field 'MovieClip.allow_comments'
        db.add_column('medialibrary_movieclip', 'allow_comments', self.gf('django.db.models.fields.CharField')(default='SITE', max_length=4), keep_default=False)

        # Adding field 'FlashMovie.creation_date'
        db.add_column('medialibrary_flashmovie', 'creation_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now(), auto_now_add=True, blank=True), keep_default=False)

        # Adding field 'FlashMovie.modification_date'
        db.add_column('medialibrary_flashmovie', 'modification_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now(), auto_now=True, blank=True), keep_default=False)

        # Adding field 'FlashMovie.allow_comments'
        db.add_column('medialibrary_flashmovie', 'allow_comments', self.gf('django.db.models.fields.CharField')(default='SITE', max_length=4), keep_default=False)

        # Adding field 'Document.creation_date'
        db.add_column('medialibrary_document', 'creation_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now(), auto_now_add=True, blank=True), keep_default=False)

        # Adding field 'Document.modification_date'
        db.add_column('medialibrary_document', 'modification_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now(), auto_now=True, blank=True), keep_default=False)

        # Adding field 'Document.allow_comments'
        db.add_column('medialibrary_document', 'allow_comments', self.gf('django.db.models.fields.CharField')(default='SITE', max_length=4), keep_default=False)

        # Adding field 'ExternalContent.creation_date'
        db.add_column('medialibrary_externalcontent', 'creation_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now(), auto_now_add=True, blank=True), keep_default=False)

        # Adding field 'ExternalContent.modification_date'
        db.add_column('medialibrary_externalcontent', 'modification_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now(), auto_now=True, blank=True), keep_default=False)

        # Adding field 'ExternalContent.allow_comments'
        db.add_column('medialibrary_externalcontent', 'allow_comments', self.gf('django.db.models.fields.CharField')(default='SITE', max_length=4), keep_default=False)

        # Adding field 'SoundTrack.creation_date'
        db.add_column('medialibrary_soundtrack', 'creation_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now(), auto_now_add=True, blank=True), keep_default=False)

        # Adding field 'SoundTrack.modification_date'
        db.add_column('medialibrary_soundtrack', 'modification_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now(), auto_now=True, blank=True), keep_default=False)

        # Adding field 'SoundTrack.allow_comments'
        db.add_column('medialibrary_soundtrack', 'allow_comments', self.gf('django.db.models.fields.CharField')(default='SITE', max_length=4), keep_default=False)

        # Adding field 'Picture.creation_date'
        db.add_column('medialibrary_picture', 'creation_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now(), auto_now_add=True, blank=True), keep_default=False)

        # Adding field 'Picture.modification_date'
        db.add_column('medialibrary_picture', 'modification_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now(), auto_now=True, blank=True), keep_default=False)

        # Adding field 'Picture.allow_comments'
        db.add_column('medialibrary_picture', 'allow_comments', self.gf('django.db.models.fields.CharField')(default='SITE', max_length=4), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'RegularFile.creation_date'
        db.delete_column('medialibrary_regularfile', 'creation_date')

        # Deleting field 'RegularFile.modification_date'
        db.delete_column('medialibrary_regularfile', 'modification_date')

        # Deleting field 'RegularFile.allow_comments'
        db.delete_column('medialibrary_regularfile', 'allow_comments')

        # Deleting field 'MovieClip.creation_date'
        db.delete_column('medialibrary_movieclip', 'creation_date')

        # Deleting field 'MovieClip.modification_date'
        db.delete_column('medialibrary_movieclip', 'modification_date')

        # Deleting field 'MovieClip.allow_comments'
        db.delete_column('medialibrary_movieclip', 'allow_comments')

        # Deleting field 'FlashMovie.creation_date'
        db.delete_column('medialibrary_flashmovie', 'creation_date')

        # Deleting field 'FlashMovie.modification_date'
        db.delete_column('medialibrary_flashmovie', 'modification_date')

        # Deleting field 'FlashMovie.allow_comments'
        db.delete_column('medialibrary_flashmovie', 'allow_comments')

        # Deleting field 'Document.creation_date'
        db.delete_column('medialibrary_document', 'creation_date')

        # Deleting field 'Document.modification_date'
        db.delete_column('medialibrary_document', 'modification_date')

        # Deleting field 'Document.allow_comments'
        db.delete_column('medialibrary_document', 'allow_comments')

        # Deleting field 'ExternalContent.creation_date'
        db.delete_column('medialibrary_externalcontent', 'creation_date')

        # Deleting field 'ExternalContent.modification_date'
        db.delete_column('medialibrary_externalcontent', 'modification_date')

        # Deleting field 'ExternalContent.allow_comments'
        db.delete_column('medialibrary_externalcontent', 'allow_comments')

        # Deleting field 'SoundTrack.creation_date'
        db.delete_column('medialibrary_soundtrack', 'creation_date')

        # Deleting field 'SoundTrack.modification_date'
        db.delete_column('medialibrary_soundtrack', 'modification_date')

        # Deleting field 'SoundTrack.allow_comments'
        db.delete_column('medialibrary_soundtrack', 'allow_comments')

        # Deleting field 'Picture.creation_date'
        db.delete_column('medialibrary_picture', 'creation_date')

        # Deleting field 'Picture.modification_date'
        db.delete_column('medialibrary_picture', 'modification_date')

        # Deleting field 'Picture.allow_comments'
        db.delete_column('medialibrary_picture', 'allow_comments')


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
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'collection categories'", 'to': "orm['collections.Collection']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('filebrowser.fields.FileBrowseField', [], {'max_length': '250', 'blank': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'children'", 'null': 'True', 'to': "orm['collections.Category']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': 'None', 'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'collections.collection': {
            'Meta': {'object_name': 'Collection'},
            'content_types': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['contenttypes.ContentType']", 'db_index': 'True', 'symmetrical': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('filebrowser.fields.FileBrowseField', [], {'max_length': '250', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'navigation_root': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': 'None', 'db_index': 'True'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
        'medialibrary.document': {
            'Meta': {'object_name': 'Document'},
            'allow_comments': ('django.db.models.fields.CharField', [], {'default': "'SITE'", 'max_length': '4'}),
            'author': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now()', 'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'document': ('filebrowser.fields.FileBrowseField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('filebrowser.fields.FileBrowseField', [], {'max_length': '100', 'blank': 'True'}),
            'modification_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now()', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'db_index': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': 'None', 'unique_with': '()', 'db_index': 'True'}),

        },
        'medialibrary.externalcontent': {
            'Meta': {'object_name': 'ExternalContent'},
            'allow_comments': ('django.db.models.fields.CharField', [], {'default': "'SITE'", 'max_length': '4'}),
            'author': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100', 'blank': 'True'}),
            'content_url': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now()', 'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('filebrowser.fields.FileBrowseField', [], {'max_length': '100', 'blank': 'True'}),
            'modification_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now()', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'db_index': 'True'}),
            'new_window': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'skip_detail': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': 'None', 'unique_with': '()', 'db_index': 'True'}),

        },
        'medialibrary.flashmovie': {
            'Meta': {'object_name': 'FlashMovie'},
            'allow_comments': ('django.db.models.fields.CharField', [], {'default': "'SITE'", 'max_length': '4'}),
            'author': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now()', 'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'flash': ('filebrowser.fields.FileBrowseField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('filebrowser.fields.FileBrowseField', [], {'max_length': '100', 'blank': 'True'}),
            'modification_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now()', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'db_index': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': 'None', 'unique_with': '()', 'db_index': 'True'}),

        },
        'medialibrary.movieclip': {
            'Meta': {'object_name': 'MovieClip'},
            'allow_comments': ('django.db.models.fields.CharField', [], {'default': "'SITE'", 'max_length': '4'}),
            'author': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now()', 'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modification_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now()', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'db_index': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': 'None', 'unique_with': '()', 'db_index': 'True'}),
            'still': ('filebrowser.fields.FileBrowseField', [], {'max_length': '100', 'blank': 'True'}),

            'video': ('filebrowser.fields.FileBrowseField', [], {'max_length': '100'})
        },
        'medialibrary.picture': {
            'Meta': {'object_name': 'Picture'},
            'allow_comments': ('django.db.models.fields.CharField', [], {'default': "'SITE'", 'max_length': '4'}),
            'author': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now()', 'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('filebrowser.fields.FileBrowseField', [], {'max_length': '100'}),
            'modification_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now()', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'db_index': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': 'None', 'unique_with': '()', 'db_index': 'True'}),

        },
        'medialibrary.regularfile': {
            'Meta': {'object_name': 'RegularFile'},
            'allow_comments': ('django.db.models.fields.CharField', [], {'default': "'SITE'", 'max_length': '4'}),
            'author': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now()', 'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'file': ('filebrowser.fields.FileBrowseField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('filebrowser.fields.FileBrowseField', [], {'max_length': '100', 'blank': 'True'}),
            'modification_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now()', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'db_index': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': 'None', 'unique_with': '()', 'db_index': 'True'}),

        },
        'medialibrary.soundtrack': {
            'Meta': {'object_name': 'SoundTrack'},
            'allow_comments': ('django.db.models.fields.CharField', [], {'default': "'SITE'", 'max_length': '4'}),
            'audio': ('filebrowser.fields.FileBrowseField', [], {'max_length': '250'}),
            'author': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now()', 'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modification_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now()', 'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'db_index': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': 'None', 'unique_with': '()', 'db_index': 'True'}),

        }
    }

    complete_apps = ['medialibrary']
