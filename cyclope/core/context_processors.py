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

from django.conf import settings
from cyclope import settings as cyc_settings

def site_settings(request):
    """Exposes all the settings in cyclope.settings to the template.
    """
    settings_dict = {}
    for setting in dir(cyc_settings):
        if setting == setting.upper() and setting.startswith('CYCLOPE'):
            settings_dict[setting] = getattr(cyc_settings, setting)
    return settings_dict


def compressor(request):
    """Exposes COMPRESS_ENABLED setting.
    """
    settings_dict = {}

    compress_enabled = settings.COMPRESS_ENABLED
    if settings.COMPRESS_DEBUG_TOGGLE and settings.COMPRESS_DEBUG_TOGGLE in request.GET:
        compress_enabled = False

    if not compress_enabled:
        settings.COMPRESS_PRECOMPILERS = tuple()
    settings_dict["COMPRESS_ENABLED"] = compress_enabled
    return settings_dict
