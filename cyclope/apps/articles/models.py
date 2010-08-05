#!/usr/bin/env python
# -*- coding: UTF-8 -*-
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


"""
apps.articles.models
--------------------
"""

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from autoslug.fields import AutoSlugField
from cyclope.core.collections.models import Collectible
from cyclope.models import BaseContent, Author, Source, Image
from cyclope.apps.medialibrary.models import Picture

YES_NO = (('YES', _('yes')), ('NO', _('no')),)


class Article(BaseContent, Collectible):
    pretitle = models.CharField(_('pre-title'), max_length=250, blank=True)
    summary = models.TextField(_('summary'), blank=True)
    text = models.TextField(_('text'))
    author = models.ForeignKey(Author, verbose_name=_('author'))
    source = models.ForeignKey(Source, verbose_name=_('source'),
                               blank=True, null=True)
    creation_date = models.DateTimeField(_('creation date'),
                                     auto_now_add=True, editable=False)
    date = models.DateTimeField(_('date'), blank=True, null=True)
    images = models.ManyToManyField(Image, null=True, blank=True,
                                    through='ArticleImageData')

    allow_comments = models.CharField(_('allow comments'), max_length=4,
                                choices = (
                                    ('SITE',_('default')),
                                    ('YES',_('enabled')),
                                    ('NO',_('disabled'))
                                ), default='SITE')

    def first_image(self):
        if self.images.count() > 0:
            return self.images.all()[0]

    class Meta:
        verbose_name = _('article')
        verbose_name_plural = _('articles')
        ordering = ('-creation_date', 'name')

class ArticleImageData(models.Model):
    article = models.ForeignKey(Article, verbose_name=_('article'))
    image = models.ForeignKey(Image, verbose_name=_('image'))
    label = models.CharField(_('label'), max_length=250)

    def __unicode__(self):
        return ""

    class Meta:
        verbose_name = _('article image')
        verbose_name_plural = _('article images')


class Attachment(models.Model):
    name = models.CharField(_('title'),max_length=250,
                             db_index=True, blank=False, unique=True)
    slug = AutoSlugField(populate_from='name', unique=True, db_index=True)
    article = models.ForeignKey(Article,
                                verbose_name=_('article'),
                                related_name=_('attachments'))
    description = models.CharField(_('description'), max_length=250,
                                   blank=True, db_index=True)
    file = models.FileField(_('file'), max_length=250, db_index=True,
                            upload_to='attachments')
    downloads = models.IntegerField(_('downloads'), default=0,
                                    blank=True, editable=False) #download counter

    def __unicode__(self):
        return '%s (%s)' % (self.name, self.file)
