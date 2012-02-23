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

from cyclope.models import BaseContent
from cyclope.core.collections.models import Collectible

DEFAULT_NUM_OF_ENTRIES = 10

class Feed(BaseContent, Collectible):
    url = models.URLField(_('URL'), max_length=250, unique=True, db_index=True)
    summary = models.TextField(_('summary'), blank=True)
    number_of_entries = models.IntegerField(_('default number of entries'), default=DEFAULT_NUM_OF_ENTRIES)
    titles_only = models.BooleanField(_('by default, only show entry titles'), default=False)

    class Meta:
        verbose_name = _('feed')
        verbose_name_plural = _('feeds')

