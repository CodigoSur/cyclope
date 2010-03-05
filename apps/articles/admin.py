# -*- coding: utf-8 -*-

from django.contrib import admin
from models import *
from django.contrib.contenttypes import generic
from django import forms
from cyclope.widgets import WYMEditor
from cyclope.core.collections.admin import CollectibleAdmin
from models import *

class ArticleForm(forms.ModelForm):
    summary = forms.CharField(widget=WYMEditor())
    text = forms.CharField(widget=WYMEditor())

    class Meta:
        model = Article

class ArticleAdmin(CollectibleAdmin):
    form = ArticleForm
    list_filter = CollectibleAdmin.list_filter + \
                  ('creation_date', 'author', 'source')
    list_display = ('name', 'is_orphan',)
    search_fields = ('name', 'pretitle', 'summary', 'text', )


admin.site.register(Article, ArticleAdmin)
admin.site.register(Author)
admin.site.register(Source)
