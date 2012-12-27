#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010-2012 Código Sur Sociedad Civil.
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
from django.contrib.contenttypes import generic

from cyclope.core.frontend import site
from cyclope.core.collections.admin import CollectibleAdmin
from cyclope.admin import BaseContentAdmin
from cyclope.apps.related_admin import GenericFKWidget, GenericModelForm
from cyclope.apps.related_admin import GenericModelChoiceField as GMCField

from models import Series, SeriesContent

def series_inline_factory(series_model):

    class SeriesContentForm(GenericModelForm):
        other_object = GMCField(label='object', widget=GenericFKWidget('other_type',
                                                       cts=series_model.get_content_models()))
        def __init__(self, *args, **kwargs):
            super(SeriesContentForm, self).__init__(*args, **kwargs)
            self.fields['other_type'].choices = series_model.get_content_types_choices()

        class Meta:
            model = SeriesContent
            fields = ('order', 'other_type', 'other_object')

    class SeriesContentInline(generic.GenericStackedInline):
        model = SeriesContent
        form = SeriesContentForm
        ct_field = 'self_type'
        ct_fk_field = 'self_id'
        extra = 0
    
    return [SeriesContentInline]


class SeriesAdmin(CollectibleAdmin, BaseContentAdmin):
    inlines = series_inline_factory(Series) + CollectibleAdmin.inlines + BaseContentAdmin.inlines
    list_display = ('name', 'creation_date') + CollectibleAdmin.list_display
    search_fields = ('name', 'description', )
    list_filter = CollectibleAdmin.list_filter + ('creation_date',)


