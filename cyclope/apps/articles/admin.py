# -*- coding: utf-8 -*-

from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy as _

from cyclope.widgets import WYMEditor, ForeignKeyImageRawIdWidget
from cyclope.core.collections.admin import CollectibleAdmin
from cyclope.admin import BaseContentAdmin
from cyclope.forms import BaseContentAdminForm
from cyclope.models import Author

from models import *


class ArticleForm(BaseContentAdminForm):
    text = forms.CharField(label=_('Text'), widget=WYMEditor())

    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        author_choices = [('', '------')]
        for author in Author.objects.all():
            if  Article in [ctype.model_class() for ctype in author.content_types.all()]:
                author_choices.append((author.id, author.name))
        self.fields['author'].choices = author_choices

    class Meta:
        model = Article


class ArticleImageDataInline(admin.StackedInline):
    model = ArticleImageData
    raw_id_fields = ('image',)
    extra = 0
    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        field = super(ArticleImageDataInline, self).formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == 'image':
            field.widget = ForeignKeyImageRawIdWidget(db_field.rel)
        return field


class ArticleAdmin(CollectibleAdmin):
    form = ArticleForm
    list_filter = CollectibleAdmin.list_filter + \
                  ('creation_date', 'author', 'source')
    list_display = ('name', 'is_orphan',)
    search_fields = ('name', 'pretitle', 'summary', 'text', )
    inlines = CollectibleAdmin.inlines + [ArticleImageDataInline]

    fieldsets = ((None,
                  {'fields': ('name', 'author', 'text', 'published')}),
                 (_('Publication data'),
                  {
                    'classes': ('collapse',),
                    'fields':('source', 'tags', 'pretitle',
                              'summary', 'date', 'allow_comments')}),
                )

admin.site.register(Article, ArticleAdmin)
admin.site.register(Author)
admin.site.register(Source)
