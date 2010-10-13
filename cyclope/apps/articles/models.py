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
    date = models.DateTimeField(_('date'), blank=True, null=True)

    def pictures(self):
        if self.related_contents:
            pic_model = models.get_model('medialibrary', 'picture')
            ctype = ContentType.objects.get_for_model(pic_model)
            rel_contents = self.related_contents.filter(other_type__pk=ctype.pk)
            return [ r.other_object for r in rel_contents ]
        else:
            return None

    class Meta:
        verbose_name = _('article')
        verbose_name_plural = _('articles')
        ordering = ('-creation_date', 'name')

