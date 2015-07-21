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

import os
from django.conf import settings
from django.contrib import admin
from django import forms
from django.db import models

from cyclope import settings as cyc_settings
from cyclope.core.collections.admin import CollectibleAdmin
from cyclope.admin import BaseContentAdmin

from models import *

from filebrowser.fields import FileBrowseField
from filebrowser.base import FileObject
from filebrowser.functions import handle_file_upload, convert_filename

# This is a standard ClearableFileInput.
# We just need to "translate" some data from the FileBrowseField
class CustomFileInput(forms.widgets.ClearableFileInput):
    def render(self, name, value, attrs=None):
        # FileBrowseField has no url attribute so we set url to url_full
        if type(value) == FileObject:
            value.url = value.url_full
        return super(CustomFileInput, self).render(name, value, attrs)


class MediaAdmin(CollectibleAdmin, BaseContentAdmin):
    inlines = CollectibleAdmin.inlines + BaseContentAdmin.inlines
    search_fields = ('name', 'description', )
    list_filter = CollectibleAdmin.list_filter + ('creation_date',)

    def get_form(self, request, obj=None, **kwargs):
        media_file_field = self.model.media_file_field
        image_file_field = self.model.image_file_field
        form = super(MediaAdmin, self).get_form(request, obj, **kwargs)
        simple_widgets = False
        if not request.user.is_superuser:
            simple_widgets = True
            form.base_fields[media_file_field].widget = CustomFileInput()
            if image_file_field:
                form.base_fields[image_file_field].widget = CustomFileInput()

        form.simple = simple_widgets
        if obj:
            form.media_file_initial = getattr(obj, media_file_field)
            # This is a hack; if the field is required it will fail validation
            # when the user does not upload a file.
            # TODO(nicoechaniz): implement proper validation for this case
            form.base_fields[media_file_field].required = False
            if image_file_field:
                form.image_file_initial = getattr(obj, image_file_field)
                form.base_fields[image_file_field].required = False
        return form

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

        def save(self, *args, **kwargs):
            # We override the standard behavior because we've overriden the FileBrowseField
            # with a simple ClearableFileInput
            if self.simple:
                abs_paths = {}
                instance = super(MediaLibraryForm, self).save(commit=False)
                image_file_field = instance.image_file_field

                file_fields = [ instance.media_file_field ]
                if image_file_field:
                    file_fields.append(image_file_field)
                for f_field in file_fields:
                    folder = media_model._meta.get_field_by_name(f_field)[0].directory
                    abs_paths[f_field] = os.path.join( 
                        settings.MEDIA_ROOT, settings.FILEBROWSER_DIRECTORY, folder
                    )
                    if f_field in self.files.keys():
                        f = self.files[f_field]
                        f.name = convert_filename(f.name)
                        name = handle_file_upload(abs_paths[f_field], f)
                        setattr(instance, f_field, name)
                    else:
                        # TODO(nicoechaniz): this is ugly! refactor
                        if f_field in ["image", "still"]:
                            if hasattr(self, "image_file_initial"):
                                setattr(instance, f_field, self.image_file_initial)
                        else:
                            if hasattr(self, "media_file_initial"):
                                setattr(instance, f_field, self.media_file_initial)
                instance.save()
                return instance
            else:
                return super(MediaLibraryForm, self).save(*args, **kwargs)

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
