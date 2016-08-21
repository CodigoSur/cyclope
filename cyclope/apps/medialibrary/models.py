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

from django.db import models
from django.utils.translation import ugettext_lazy as _

from filebrowser.fields import FileBrowseField

from cyclope.models import BaseContent, Author, Source
from cyclope.core.collections.models import Collectible
from cyclope.utils import ThumbnailMixin, get_extension
import cyclope.apps.abuse
from datetime import datetime

class BaseMedia(BaseContent, Collectible, ThumbnailMixin):
    """Abstract class for media content.
    """
    author = models.ForeignKey(Author, verbose_name=_('author'),
                               null=True, blank=True, on_delete=models.SET_NULL)
    source = models.ForeignKey(Source, verbose_name=_('source'),
                               blank=True, null=True, on_delete=models.SET_NULL)
    description = models.TextField(_('description'), blank=True)

    media_file_field = None # This must me set to the media_file on the model
                            # (eg: "audio" for Soundtrack)
    image_file_field = "image" # This must me set to the image_file on the model
                               # if the field name is not "image"
                               # (eg: "still" for MovieClip)
    directory = None # Tells where in media/ to create this Content Type's directory structure
                     # TODO(NumericA) auto - lower case class name hypenated

    @property
    def media_file(self):
        return getattr(self, self.media_file_field)

    @property
    def file_type(self):
        return get_extension(self.media_file.path)

    class Meta:
        abstract = True
        ordering = ('-creation_date', 'name')


class DateFileBrowseField(FileBrowseField):
    # TODO(NumericA) to cyclope_utils.py
    def _get_todays_folder(self, path):
        """
        generate path/year/month directory structure
        ex. /media/pictures/2016/8
        """
        return path+"/{:%Y/%m}".format(datetime.now())
        
    def __init__(self, *args, **kwargs):
        super(DateFileBrowseField, self).__init__(*args, **kwargs)
        self.directory = self._get_todays_folder(self.directory)

class Picture(BaseMedia):
    """Picture model.
    """
    directory='pictures/'
    image = DateFileBrowseField(_('image'), max_length=100, format='Image', directory='pictures/')
    media_file_field = "image"
    image_file_field = None

    class Meta:
        verbose_name = _('picture')
        verbose_name_plural = _('pictures')

class SoundTrack(BaseMedia):
    """AudioTrack model.
    """
    directory='sound_tracks/'
    audio = DateFileBrowseField(_('audio'), max_length=250, format='Audio', directory='sound_tracks/')
    image = DateFileBrowseField(_('image'), max_length=100, format='Image', directory='pictures/', blank=True, null=True)
    media_file_field = "audio"

    class Meta:
        verbose_name = _('sound track')
        verbose_name_plural = _('sound tracks')


class MovieClip(BaseMedia):
    """MovieClip model.
    """
    directory='movie_clips/'
    still = DateFileBrowseField(_('still'), max_length=100, format='Image', directory='pictures/', blank=True)
    video = DateFileBrowseField(_('video'), max_length=100, format='Video', directory='movie_clips/')
    media_file_field = "video"
    image_file_field = "still"

    def image(self):
        return self.still

    def get_thumbnail_src(self):
        return self.still.url_thumbnail

    class Meta:
        verbose_name = _('movie clip')
        verbose_name_plural = _('movie clips')


class Document(BaseMedia):
    """Document model.
    """
    directory='documents/'
    image = DateFileBrowseField(_('image'), max_length=100, format='Image', directory='pictures/', blank=True)
    document = DateFileBrowseField(_('document'), max_length=100, format='Document', directory='documents/')
    media_file_field = "document"

    class Meta:
        verbose_name = _('document')
        verbose_name_plural = _('documents')


class FlashMovie(BaseMedia):
    """FlashMovie model.
    """
    directory='flashmovies/'
    image = DateFileBrowseField(_('image'), max_length=100, format='Image', directory='pictures/', blank=True)
    flash = DateFileBrowseField(_('flash'), max_length=100, format='Flash',directory='flashmovies/', blank=True)
    media_file_field = "flash"

    class Meta:
        verbose_name = _('flash movie')
        verbose_name_plural = _('flash movies')


class RegularFile(BaseMedia):
    """RegularFile model. Accepts any type of file.
    """
    directory='regular_files/'
    image = DateFileBrowseField(_('image'), max_length=100, format='Image', directory='pictures/', blank=True)
    file = DateFileBrowseField(_('file'), max_length=100, directory='regular_files/')
    media_file_field = "file"

    class Meta:
        verbose_name = _('file')
        verbose_name_plural = _('files')


class ExternalContent(BaseMedia):
    """ExternalContent. For media that's displayed with custom html.
    """
    image = DateFileBrowseField(_('image'), max_length=100, format='Image', directory='pictures/', blank=True)
    content_url = models.CharField(_('content url'), max_length=100)
    new_window = models.BooleanField(_('open in new window'), default=False)
    skip_detail = models.BooleanField(_('skip detailed view'), default=False)
    media_file_field = "content_url"

    class Meta:
        verbose_name = _('external content')
        verbose_name_plural = _('external contents')

actual_models = [Picture, SoundTrack, MovieClip, Document, FlashMovie,
                 RegularFile, ExternalContent]
