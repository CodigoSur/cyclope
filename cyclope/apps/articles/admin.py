# -*- coding: utf-8 -*-

from django.contrib import admin
from django import forms
from django.utils.translation import ugettext as _

from cyclope.widgets import WYMEditor
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


class ArticleAdmin(CollectibleAdmin):
    form = ArticleForm
    list_filter = CollectibleAdmin.list_filter + \
                  ('creation_date', 'author', 'source')
    list_display = ('name', 'is_orphan',)
    search_fields = ('name', 'pretitle', 'summary', 'text', )
#    inlines = CollectibleAdmin.inlines + [PictureInline]
    raw_id_fields = ('pictures',)

admin.site.register(Article, ArticleAdmin)
admin.site.register(Author)
admin.site.register(Source)
