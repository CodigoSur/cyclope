#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010 Código Sur - Nuestra América Asoc. Civil / Fundación Pacificar.
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
from cyclope.admin import BaseContentAdmin
from cyclope import settings as cyc_settings

from models import *

class FeedAdmin(CollectibleAdmin, BaseContentAdmin):
    list_display = ('name', 'url')
    search_fields = ('name', 'url', 'summary')
    inlines = CollectibleAdmin.inlines + BaseContentAdmin.inlines

    fieldsets = ((None,
                  {'fields': ('name', 'url', 'number_of_entries', 'titles_only')}),
                 (_('Publication data'),
                  {
                    'classes': ('collapse',),
                    'fields':( 'published', 
                              'summary', 'allow_comments', 'creation_date')}),
                )

admin.site.register(Feed, FeedAdmin)
