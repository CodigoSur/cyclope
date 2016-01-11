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

"""
Based on patches #9976 (https://code.djangoproject.com/ticket/9976)

"""

import re

from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.widgets import ForeignKeyRawIdWidget

from cyclope.apps.related_admin.views import do_render_object
from cyclope.apps.related_admin import GenericFKWidget, GenericModelForm
from cyclope.apps.related_admin import GenericModelChoiceField as GMCField

class SearchAndCreateFKWidget(GenericFKWidget):
    def render(self, name, value, attrs):
        out = super(SearchAndCreateFKWidget, self).render(name, value, attrs)
        remove_picture = """<div class='remove_picture' onClick="$('#id_%s').val('');$('#id_%s').siblings('.object-representation').empty();">%s</div>""" % (name, name, ugettext(u"Remove"))
        name = "%s_none" % name
        picture_content_type_id = ContentType.objects.get_by_natural_key("medialibrary", "picture").id
        fake_ctfield = "<select id='id_{0}' name='{0}' style='display:none'><option value='{1}'>Picture</option></select>".format(name, picture_content_type_id)
        return mark_safe("<fieldset class='inlined'>" + fake_ctfield + out + remove_picture + "</fieldset>")

    def get_actual_object(self, value):
        try:
            actual_object = FakeGMCField.to_python(value)
        except forms.ValidationError:
            actual_object = None
        return actual_object

class FakeGMCField(GMCField):
    def __init__(self, queryset, *args, **kwargs):
        self.queryset = queryset
        super(FakeGMCField, self).__init__(*args, **kwargs)

    def prepare_value(self, value):
        if value and not value == "None" and not isinstance(value, models.Model):
            value = self.queryset.get(pk=value)
        return super(FakeGMCField, self).prepare_value(value)

class ArticleForm(GenericModelForm):
    picture = FakeGMCField(queryset=Picture.objects.all(), widget=SearchAndCreateFKWidget("picture_none", [Picture]),
                           required=False)

    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        author_choices = [('', '------')]
        for author in Author.objects.all():
            if  Article in [ctype.model_class() for ctype in author.content_types.all()]:
                author_choices.append((author.id, author.name))
        self.fields['author'].choices = author_choices

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
                  {'fields': ('name', 'author', 'published', 'pretitle', 'picture',
                      'summary', 'text' )}),
                 (_('Publication data'),
                  {
                    'classes': ('collapse',),
                    'fields':('slug', 'show_author', 'source',
                              'date', 'allow_comments', 'creation_date')}),
                )

    class Media:
        css = {
            'all' : (cyc_settings.CYCLOPE_STATIC_URL + 'css/jquery-ui-1.11.4.min.css',)
        }        
        js =(
            cyc_settings.CYCLOPE_STATIC_URL + 'js/cyclope_media_widget.js',       
        )        

admin.site.register(Article, ArticleAdmin)
