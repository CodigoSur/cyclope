# -*- coding: utf-8 -*-
#
# Copyright 2012 Código Sur Sociedad Civil
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

import os
import sys
import imp

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, ImproperlyConfigured
from django.utils.translation import ugettext_lazy as _

_default_cache = None
_local_cache = None

_DEFAULT_THEMES_ROOT = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                    "templates", "cyclope", "themes")

def _get_themes(path):
    names = [item for item in os.listdir(path) if os.path.isdir(os.path.join(path, item))]
    themes_ = {}
    for name in names:
        filename = os.path.join(path, name, "__init__.py")
        themes_[name] = imp.load_source(name, filename)
    return themes_

def get_default_themes():
    global _default_cache
    path = _DEFAULT_THEMES_ROOT
    if _default_cache is None:
        _default_cache = _get_themes(path)
    return _default_cache

def get_local_themes(cache=True):
    global _local_cache
    if not hasattr(settings, 'CYCLOPE_LOCAL_THEMES_DIR'):
        return {}
    path = settings.CYCLOPE_LOCAL_THEMES_DIR
    if _local_cache is None or not cache:
        _local_cache = _get_themes(path)
    return _local_cache

def get_all_themes(cache_local=True):
    """
    Returns a dictionary with all themes. Key are the theme name (directory name)
    and value the module object.
    """
    all_themes = get_default_themes()
    all_themes.update(get_local_themes(cache_local))
    return all_themes

def get_theme(name):
    """
    Get a theme module by its name.
    """
    return get_all_themes().get(name, None)


if hasattr(settings, 'CYCLOPE_LOCAL_THEMES_DIR'):
    if not hasattr(settings, 'CYCLOPE_LOCAL_THEMES_MEDIA_PREFIX'):
        raise ImproperlyConfigured(_('You need to set CYCLOPE_LOCAL_THEMES_PREFIX'\
                                      ' in your settings file'))


    if not os.path.exists(settings.CYCLOPE_LOCAL_THEMES_DIR):
        raise ImproperlyConfigured(_('Your CYCLOPE_LOCAL_THEMES_DIR' \
                                      'setting is invalid'))
