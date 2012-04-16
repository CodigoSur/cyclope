#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010-2012 Código Sur - Nuestra América Asoc. Civil / Fundación Pacificar.
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

# based on  shestera's django-multisite
# http://github.com/shestera/django-multisite

import os
import sys
import imp

from django.conf import settings
import cyclope.settings as cyc_settings

from django.utils.importlib import import_module
from django.utils.cache import patch_vary_headers

from django.contrib import admin

from cyclope.core.multisite.threadlocals import DynamicSetting
from cyclope import default_settings

class DynamicSettingsMiddleware(object):
    _path = sys.path[:]

    def process_request(self, request):
        host = request.get_host()
        shost = host.rsplit(':', 1)[0] # only host, without port
        settings.REQUEST_HOST.set(shost)
        SITE_BASE_PATH = os.path.realpath(os.path.join(settings.CYCLOPE_MULTISITE_BASE_PATH,
                                                       shost, "cyclope_project"))
        settings.MEDIA_ROOT.set('%s/media/' % SITE_BASE_PATH)

        site_settings = imp.load_source("site_settings", '%s/settings.py' % SITE_BASE_PATH)

        CYCLOPE_SITE_SETTINGS = cyc_settings.get_site_settings()
        cyc_settings.populate_from_site_settings(CYCLOPE_SITE_SETTINGS)

        admin.autodiscover()
        for setting_name in dir(site_settings):
            if setting_name == setting_name.upper():
                old_value = getattr(settings, setting_name, None)
                new_value = getattr(site_settings, setting_name)

                # this is a dynamic setting
                if issubclass(type(old_value), DynamicSetting):
                    # the current site did not override the default
                    if issubclass(type(new_value), DynamicSetting):
                        old_value.set(getattr(default_settings, setting_name))
                    else:
                        old_value.set(new_value)
                else:
                    setattr(settings, setting_name, new_value)

        cyc_settings.reload_settings()

        # Hack sys path for urls import
        sys.path = self._path[:]
        sys.path.insert(0, SITE_BASE_PATH)
        urlconf = 'urls'
        request.urlconf = urlconf

    def process_response(self, request, response):
        if getattr(request, "urlconf", None):
            patch_vary_headers(response, ('Host',))
        return response
