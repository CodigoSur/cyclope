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

from django.db import models
from django.utils.translation import ugettext_lazy as _

from autoslug.fields import AutoSlugField

from cyclope.models import BaseContent
from cyclope.core.collections.models import Collectible

class StaticPage(BaseContent, Collectible):
    summary = models.TextField(_('summary'), blank=True)
    text = models.TextField(_('text'))

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('static page')
        verbose_name_plural = _('static pages')


class HTMLBlock(models.Model):
    name = models.CharField(_('name'), max_length=250,
                             db_index=True, blank=False)
    slug = AutoSlugField(populate_from='name', unique=True,
                         db_index=True, always_update=True)    
    text = models.TextField(_('text'))
    
    def get_absolute_url(self):
        return '/%s/%s/' % (self._meta.object_name.lower(), self.slug)
    
    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('html block')
        verbose_name_plural = _('html blocks')

