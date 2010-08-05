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

from django.db import models
from django.utils.translation import ugettext as _

from cyclope.models import BaseContent
from cyclope.core.collections.models import Collectible

class Color(BaseContent):
    pass

class Shoe(BaseContent, Collectible):
    cut = models.CharField(_('cut'), max_length=100, blank=True)
    material = models.CharField(_('material'), max_length=100, blank=True)
    sole = models.CharField(_('sole'), max_length=100, blank=True)
    colors = models.ManyToManyField(Color, blank=True, null=True)
    heel = models.CharField(_('heel'), max_length=10, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('shoe')
        verbose_name_plural = _('shoes')
