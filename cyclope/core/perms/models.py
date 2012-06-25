#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2012 Código Sur Asoc. Civil
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
core.perms.models
-------------------
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from cyclope.core.collections.models import Category


class CategoryPermission(models.Model):
    user = models.ForeignKey(User, verbose_name=_('user'))
    can_edit_content = models.BooleanField(_('can edit content'))
    can_add_content = models.BooleanField(_('can add content'))
    category = models.ForeignKey(Category, verbose_name=_('category'))

    class Meta:
        unique_together = ('category', 'user')
        verbose_name = _('category permission')
        verbose_name_plural = _('category permissions')
