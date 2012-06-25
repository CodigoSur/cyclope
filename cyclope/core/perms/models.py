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
from cyclope.core.collections.models import Category


class CategoryPermission(models.Model):
    user = models.ForeignKey(User)
    can_edit_content = models.BooleanField()
    can_add_content = models.BooleanField()    
    category = models.ForeignKey(Category)

    def _available_perms(self):
        return [ f.name for f in self.fields if f.name.startswith('can_') ]

    available_perms = property(_available_perms)

    class Meta:
        unique_together = ('category', 'user')

