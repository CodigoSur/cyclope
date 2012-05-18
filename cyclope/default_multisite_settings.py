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

"""This file holds default values for multisite deployments
"""

from cyclope.default_settings import *
from cyclope.core.multisite.threadlocals import RequestHostHook, DynamicSetting

REQUEST_HOST = RequestHostHook()


MIDDLEWARE_CLASSES = ('cyclope.core.multisite.middleware.DynamicSettingsMiddleware',) + \
                     MIDDLEWARE_CLASSES

DATABASE_ROUTERS = ['cyclope.core.multisite.dbrouters.MultiSiteRouter',]


# when first running the multisite project, REQUEST_HOST is empty
if REQUEST_HOST.get_module_name():
    HAYSTACK_SITECONF = '%s.%s' % (REQUEST_HOST.get_module_name(), 'cyclope_project.search_sites')
else:
    HAYSTACK_SITECONF = 'cyclope_project.search_sites'


CYCLOPE_PAGINATION = DynamicSetting('CYCLOPE_PAGINATION', dict)
