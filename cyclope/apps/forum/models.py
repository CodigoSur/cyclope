#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010-2012 Código Sur Asociación Civil
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
apps.forum.models
--------------------
"""

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from cyclope.core.collections.models import Collectible

from cyclope.models import BaseContent


class Topic(BaseContent, Collectible):
    text = models.TextField(_('text'))

    class Meta:
        verbose_name = _('topic')
        verbose_name_plural = _('topics')
        ordering = ('-creation_date',)
