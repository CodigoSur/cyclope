#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010-2013 Código Sur Sociedad Civil.
# All rights reserved.
#
# This file is part of Cyclope.
#
# Cyclope is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Cyclope is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy as _

from cyclope.core.collections.admin import CollectibleAdmin
from cyclope.models import Author
from cyclope.admin import BaseContentAdmin
from cyclope import settings as cyc_settings

from models import *

import re

from cyclope.apps.media_widget import MediaWidget, MediaWidgetField

class ArticleForm(forms.ModelForm):

    pictures = MediaWidgetField(
        label = _('Article\'s images'),
        queryset=Picture.objects.all(), 
        widget=MediaWidget(), 
        required=False
    )

    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        # Author
        author_choices = [('', '------')]
        for author in Author.objects.all():
            if Article in [ctype.model_class() for ctype in author.content_types.all()]:
                author_choices.append((author.id, author.name))
        self.fields['author'].choices = author_choices
        # Pictures default
        if not kwargs.has_key('instance'):
            self.initial['pictures'] = []

    class Meta:
        model = Article

class ArticleAdmin(CollectibleAdmin, BaseContentAdmin):
    form = ArticleForm
    list_filter = CollectibleAdmin.list_filter + \
                  ('creation_date', 'author', 'source')
    list_display = ('name', 'published', 'translations', 'creation_date') + \
                   CollectibleAdmin.list_display
    search_fields = ('name', 'pretitle', 'summary', 'text', )

    inlines = CollectibleAdmin.inlines + BaseContentAdmin.inlines

    fieldsets = ((None,
                  {'fields': ('name', 'author', 'published', 'pretitle', 'pictures',
                      'summary', 'text' )}),
                 (_('Publication data'),
                  {
                    'classes': ('collapse',),
                    'fields':('slug', 'show_author', 'source',
                              'date', 'allow_comments', 'creation_date')}),
                )

    class Media:
        css = {
            'all' : (cyc_settings.CYCLOPE_JQUERY_UI_CSS_PATH,
                    'css/media_widget.css')
        }

admin.site.register(Article, ArticleAdmin)
