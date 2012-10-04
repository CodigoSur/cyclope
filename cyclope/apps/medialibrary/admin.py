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
from django import forms

from cyclope.core.collections.admin import CollectibleAdmin
from cyclope.admin import BaseContentAdmin

from models import *

class MediaAdmin(CollectibleAdmin, BaseContentAdmin):
    inlines = CollectibleAdmin.inlines + BaseContentAdmin.inlines
    search_fields = ('name', 'description', )
    list_filter = CollectibleAdmin.list_filter + ('creation_date',)

has_thumbnail = [Picture, MovieClip, FlashMovie]
def media_admin_factory(media_model):
    class MediaLibraryForm(forms.ModelForm):
        def __init__(self, *args, **kwargs):
            super(MediaLibraryForm, self).__init__(*args, **kwargs)
            author_choices = [('', '------')]
            for author in Author.objects.all():
                if media_model in [ctype.model_class()
                                   for ctype in author.content_types.all()]:
                    author_choices.append((author.id, author.name))
            self.fields['author'].choices = author_choices

        class Meta:
            model = media_model
            

    if media_model in has_thumbnail:
        list_display = ['name', 'thumbnail']
    else:
        list_display = ['name']
    list_display += CollectibleAdmin.list_display

    return type('%sAdmin' % media_model.__name__,
                (MediaAdmin,),
                {'form': MediaLibraryForm, 'list_display': list_display})

admin.site.register(Picture, media_admin_factory(Picture))
admin.site.register(SoundTrack, media_admin_factory(SoundTrack))
admin.site.register(MovieClip, media_admin_factory(MovieClip))
admin.site.register(Document, media_admin_factory(Document))
admin.site.register(FlashMovie, media_admin_factory(FlashMovie))
admin.site.register(RegularFile, media_admin_factory(RegularFile))
admin.site.register(ExternalContent, media_admin_factory(ExternalContent))
