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

"""
Default and dynamic (db based) settings.

All settings will be available to templates if the site_settings context processor is installed.

Attributes:

  Overidable by the project settings.py:

    CYCLOPE_PREFIX: prefix for cyclope URLs, defaults to 'cyclope/'
    CYCLOPE_MEDIA_URL: URL to cyclope media files
    CYCLOPE_MEDIA_ROOT: defaults to cyclope/ folder of the project's MEDIA_ROOT
    CYCLOPE_THEMES_ROOT: path to the themes package

  Automatic (based on database values):

    CYCLOPE_SITE_SETTINGS: the SiteSettings instance
    CYCLOPE_CURRENT_THEME
    CYCLOPE_THEME_MEDIA_URL
    CYCLOPE_DEFAULT_LAYOUT
    CYCLOPE_DEFAULT_TEMPLATE
"""
import sys, os

from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save, pre_delete

from cyclope.models import SiteSettings

from cyclope.core.frontend.sites import site

settings.TEMPLATE_DIRS += (os.path.join(os.path.dirname(__file__), 'templates'),)

CYCLOPE_PREFIX = getattr(settings, 'CYCLOPE_PREFIX',
                           'cyclope/')
CYCLOPE_MEDIA_URL = getattr(settings, 'CYCLOPE_MEDIA_URL',
                           '%scyclope/' % settings.MEDIA_URL)
CYCLOPE_MEDIA_ROOT = getattr(settings, 'CYCLOPE_MEDIA_ROOT',
                            '%scyclope/' % settings.MEDIA_ROOT)
CYCLOPE_THEMES_ROOT = getattr(settings, 'CYCLOPE_THEMES_ROOT',
                              os.path.join(os.path.dirname(__file__),
                                           "templates/cyclope/themes/"))
CYCLOPE_STATICPAGE_TEXT_STYLE = getattr(settings,
                                            'CYCLOPE_STATICPAGE_TEXT_STYLE',
                                            'textile'
                                            )
CYCLOPE_ARTICLE_TEXT_STYLE = getattr(settings,
                                            'CYCLOPE_ARTICLE_TEXT_STYLE',
                                            'textile'
                                            )
# pagination
CYCLOPE_PAGINATION = getattr(settings, 'CYCLOPE_PAGINATION',
                             { 'TEASER' : 10,
                               'LABELED_ICON' : 30,})

#TODO(nicoechaniz): re-evaluate the way we are handling these dynamic settings, it is practical but seems hacky and error-prone.

sys.path.append(os.path.join(CYCLOPE_THEMES_ROOT, '../'))
#import themes as CYCLOPE_THEMES
import themes

#TODO(nicoechaniz): adapt for multi-site.
def get_site_settings():
    """Get the SiteSettings object.

    Returns:
        SiteSettings instance or None if no SiteSettings have been created.

    """
    from django.core.exceptions import ObjectDoesNotExist
    from django.db.utils import DatabaseError
    try:
        #TODO(nicoechaniz): Fix for multi-site
        site_settings = SiteSettings.objects.all()[0]
    # catch exceptions if the database is not available or no settings created
    except (DatabaseError, IndexError):
        site_settings = None

    return site_settings

CYCLOPE_BASE_CONTENT_TYPES = site.base_content_types

CYCLOPE_SITE_SETTINGS = get_site_settings()

# If the site has already been set up we read some settings
# and make them available at module level
if CYCLOPE_SITE_SETTINGS is not None:
    CYCLOPE_CURRENT_THEME = CYCLOPE_SITE_SETTINGS.theme
    if CYCLOPE_CURRENT_THEME in themes.local_themes:
        CYCLOPE_THEME_MEDIA_URL = '%s%s/' % (
            settings.CYCLOPE_LOCAL_THEMES_MEDIA_PREFIX, CYCLOPE_CURRENT_THEME)
    else:
        CYCLOPE_THEME_MEDIA_URL = '%sthemes/%s/' % (CYCLOPE_MEDIA_URL,
                                                    CYCLOPE_CURRENT_THEME)

    CYCLOPE_THEME_PREFIX = 'cyclope/themes/%s/' % CYCLOPE_CURRENT_THEME
    CYCLOPE_THEME_BASE_TEMPLATE = 'cyclope/themes/%s/base.html' \
                                   % CYCLOPE_CURRENT_THEME

    if CYCLOPE_SITE_SETTINGS.default_layout_id:
        CYCLOPE_DEFAULT_LAYOUT = CYCLOPE_SITE_SETTINGS.default_layout

        CYCLOPE_DEFAULT_TEMPLATE = 'cyclope/themes/%s/%s' % (
            CYCLOPE_CURRENT_THEME,
            CYCLOPE_DEFAULT_LAYOUT.template)

def _refresh_site_settings(sender, instance, created, **kwargs):
    "Callback to refresh site settings when they are modified in the database"
    # we remove our keys from globals, otherwise deleted db_based settings don't
    # get deleted at module level
    if not kwargs.get('raw', True):
        cyc_keys = [ key for key in globals() if key.startswith('CYCLOPE')]
        for key in cyc_keys:
            globals().pop(key)
        import sys
        reload(sys.modules[__name__])

post_save.connect(_refresh_site_settings, sender=SiteSettings)

from django.contrib.contenttypes.models import ContentType
from cyclope.models import RelatedContent

def _delete_related_contents(sender, instance, **kwargs):
    # cascade delete does not delete the RelatedContent elements
    # where this object is the related content, so we do it here.
    ctype = ContentType.objects.get_for_model(sender)
    if hasattr(instance, 'id'):
        print "instance:", instance.id
        related_from = RelatedContent.objects.filter(other_type=ctype,
                                                    other_id=instance.id)
        for obj in related_from:
            obj.delete()

pre_delete.connect(_delete_related_contents)
