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

from django.conf import settings as django_settings
import cyclope.settings as cyc_settings

from django.utils.importlib import import_module
from django.utils.cache import patch_vary_headers

from django.contrib import admin

from cyclope.core.multisite.threadlocals import DynamicSetting
from cyclope import default_settings
from cyclope import themes

class DynamicSettingsMiddleware(object):
    _path = sys.path[:]

    def process_request(self, request):
        host = request.get_host()
        shost = host.rsplit(':', 1)[0] # only host, without port
        django_settings.REQUEST_HOST.set(shost)
        SITE_BASE_PATH = os.path.realpath(os.path.join(django_settings.CYCLOPE_MULTISITE_BASE_PATH,
                                                       shost, "cyclope_project"))
        django_settings.MEDIA_ROOT.set('%s/media/' % SITE_BASE_PATH)
        try:
            settings_filename = '%s/settings.py' % SITE_BASE_PATH
            site_settings = imp.load_source("site_settings", settings_filename)
        except IOError:
            raise ValueError("Settings for host %s not found at %s " %
                                                            (shost,
                                                             settings_filename))


        CYCLOPE_SITE_SETTINGS = cyc_settings.get_site_settings()

        admin.autodiscover()
        replace_settings(django_settings, site_settings)
        cyc_settings.reload_settings()
        cyc_settings.populate_from_site_settings(CYCLOPE_SITE_SETTINGS)

        # Hack sys path for urls import
        sys.path = self._path[:]
        sys.path.insert(0, SITE_BASE_PATH)
        urlconf = 'urls'
        request.urlconf = urlconf

    def process_response(self, request, response):
        if getattr(request, "urlconf", None):
            patch_vary_headers(response, ('Host',))
        return response

def replace_settings(old_settings, new_settings):
    """
    Updates old_settings values with new_settings's using DynamicSettings.
    """
    for setting_name in dir(new_settings):
        if setting_name == setting_name.upper():
            old_value = getattr(old_settings, setting_name, None)
            new_value = getattr(new_settings, setting_name)

            # this is a dynamic setting
            if issubclass(type(old_value), DynamicSetting):
                # the current site did not override the default
                if issubclass(type(new_value), DynamicSetting):
                    old_value.set(getattr(default_settings, setting_name))
                else:
                    old_value.set(new_value)
            else:
                setattr(old_settings, setting_name, new_value)

