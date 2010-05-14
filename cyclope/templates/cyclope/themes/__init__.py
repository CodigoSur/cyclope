# *-- coding:utf-8 --*
"""Theme configurations."""

import os, sys
from django.utils import importlib
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, ImproperlyConfigured
from django.utils.translation import ugettext as _

# hacky stuff...

# skip __init.py and __init__.pyc
available = [ item for item in os.listdir(
    os.path.join(os.path.dirname(__file__))
    )
             if not item.startswith('__init__.py')]

local_themes = []
if hasattr(settings, 'CYCLOPE_LOCAL_THEMES_DIR'):
    print "has"
    if not hasattr(settings, 'CYCLOPE_LOCAL_THEMES_MEDIA_PREFIX'):
        raise ImproperlyConfigured(
         _('You need to set CYCLOPE_LOCAL_THEMES_PREFIX in your settings file'))
    local_themes_dir = settings.CYCLOPE_LOCAL_THEMES_DIR
    sys.path.append(local_themes_dir)
    print local_themes_dir
    local_themes = [
        item for item in
        os.listdir(os.path.join(os.path.dirname(local_themes_dir)))
        if not item.startswith('__init__.py') and not item in available ]

    available.extend(local_themes)

for theme in available:
#    importlib.import_module(theme)
    print theme
    exec 'import %s' % theme

