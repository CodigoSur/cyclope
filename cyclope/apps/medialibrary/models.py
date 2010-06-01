# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.contenttypes.models import ContentType

from autoslug.fields import AutoSlugField
#from imagekit.models import ImageModel
from filebrowser.fields import FileBrowseField

from cyclope.models import BaseContent
from cyclope.core.collections.models import Collectible

class BaseMedia(BaseContent, Collectible):
    """Abstract class for media content.
    """
    author = models.CharField(_('author'), max_length=100,
                               db_index=True, blank=True)
    description = models.TextField(_('description'), blank=True)

    class Meta:
        abstract = True


class Picture(BaseMedia):
    """Picture model.
    """
    image =  FileBrowseField(_('image'), max_length=100, format='Image',
                             directory='pictures/')

    class Meta:
        verbose_name = _('picture')
        verbose_name_plural = _('pictures')


class SoundTrack(BaseMedia):
    """AudioTrack model.
    """
#   image = FileBrowseField(_('image'), max_length=100, format='Image',
#                             directory='pictures/')
    audio =  FileBrowseField(_('audio'), max_length=250, format='Audio',
                             directory='sound_tracks/')

    class Meta:
        verbose_name = _('sound track')
        verbose_name_plural = _('sound tracks')


class MovieClip(BaseMedia):
    """MovieClip model.
    """
    still = FileBrowseField(_('still'), max_length=100, format='Image',
                            directory='movie_stills/', blank = True)
    video =  FileBrowseField(_('video'), max_length=100, format='Video',
                             directory='movie_clips/')

    class Meta:
        verbose_name = _('movie clip')
        verbose_name_plural = _('movie clips')


class Document(BaseMedia):
    """Document model.
    """
    image = FileBrowseField(_('image'), max_length=100, format='Image',
                            directory='document_images/', blank=True)
    document =  FileBrowseField(_('document'), max_length=100, format='Document',
                            directory='documents/')

    class Meta:
        verbose_name = _('document')
        verbose_name_plural = _('documents')


class FlashMovie(BaseMedia):
    """FlashMovie model.
    """
    image = FileBrowseField(_('image'), max_length=100, format='Image',
                            directory='flashmovie_images/', blank=True)
    flash =  FileBrowseField(_('flash'), max_length=100, format='Flash',
                                  directory='flashmovies/')

    class Meta:
        verbose_name = _('flash movie')
        verbose_name_plural = _('flash movies')


class RegularFile(BaseMedia):
    """RegularFile model. Accepts any type of file.
    """
    image = FileBrowseField(_('image'), max_length=100, format='Image',
                            directory='regular_file_images/', blank=True)
    file =  FileBrowseField(_('file'), max_length=100,
                            directory='regular_files/')

    class Meta:
        verbose_name = _('file')
        verbose_name_plural = _('files')
