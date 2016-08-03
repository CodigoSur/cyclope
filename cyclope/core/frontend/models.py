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

"""
core.frontend.models
--------------------
"""

from django.db.models.signals import post_save
from cyclope.models import MenuItem

def _refresh_site_urls(sender, instance, created, **kwargs):
    "Callback to refresh site url patterns when a MenuItem is modified"
    from django.conf import settings
    import sys
    try:
        return reload(sys.modules[settings.ROOT_URLCONF])
    except KeyError:
        # fails when testing...
        pass

post_save.connect(_refresh_site_urls, sender=MenuItem, dispatch_uid="cyclope.core.frontend.sites")
