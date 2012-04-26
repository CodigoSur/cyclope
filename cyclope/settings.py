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

"""
Default and dynamic (db based) settings.

CYCLOPE_* settings will be available to templates through the site_settings context processor.

Attributes:

  Overidable by the project settings.py:

    CYCLOPE_PROJECT_PATH: path to the django project that will be serving Cyclope
    CYCLOPE_PREFIX: prefix for Cyclope URLs, defaults to 'cyclope/'
    CYCLOPE_STATIC_URL: URL to Cyclope static files
    CYCLOPE_STATIC_ROOT: defaults to cyclope/ folder of the project's STATIC_ROOT
    CYCLOPE_THEMES_ROOT: path to the themes package

  Automatic (based on database values):

    CYCLOPE_PROJECT_NAME
    CYCLOPE_SITE_SETTINGS: the SiteSettings instance
    CYCLOPE_CURRENT_THEME
    CYCLOPE_THEME_MEDIA_URL
    CYCLOPE_DEFAULT_LAYOUT
    CYCLOPE_DEFAULT_TEMPLATE
    CYCLOPE_CONTACTS_PROFILE_MODULE
    CYCLOPE_CONTACTS_PROFILE_ADMIN_INLINE_MODULE
    CYCLOPE_CONTACTS_PROFILE_TEMPLATE

"""

import sys, os

from django.conf import settings
from django.utils.translation import ugettext_lazy as _, ugettext
from django.db.models.signals import post_save, pre_delete
from django.core.exceptions import ImproperlyConfigured
from django.db.utils import DatabaseError
from django.db.models import get_model

from cyclope.models import SiteSettings

from cyclope.core.frontend.sites import site

CYCLOPE_PREFIX = getattr(settings, 'CYCLOPE_PREFIX',
                           'cyclope/')
CYCLOPE_STATIC_URL = getattr(settings, 'CYCLOPE_STATIC_URL',
                             '%scyclope/' % settings.STATIC_URL)
CYCLOPE_STATIC_ROOT = getattr(settings, 'CYCLOPE_STATIC_ROOT',
                            '%scyclope/' % settings.MEDIA_ROOT)

# For backwards compatibility only!
CYCLOPE_MEDIA_URL =  CYCLOPE_STATIC_URL
CYCLOPE_MEDIA_ROOT = CYCLOPE_STATIC_ROOT


# FIXME #120: STATIC_ROOT is pointing to MEDIA_ROOT because some
# apps doesn't upgraded to static django 1.3 convention.
CYCLOPE_THEMES_ROOT = getattr(settings, 'CYCLOPE_THEMES_ROOT',
                              os.path.join(os.path.dirname(__file__),
                                           "templates/cyclope/themes/"))
CYCLOPE_TEXT_STYLE = getattr(settings, 'CYCLOPE_TEXT_STYLE', 'textile')

# For backwards compatibility only!
CYCLOPE_ARTICLE_TEXT_STYLE = getattr(settings, 'CYCLOPE_TEXT_STYLE', 'textile')
CYCLOPE_STATICPAGE_TEXT_STYLE = getattr(settings, 'CYCLOPE_TEXT_STYLE', 'textile')

# Contacts Profile
CYCLOPE_CONTACTS_PROFILE_MODULE = getattr(settings, 'CYCLOPE_CONTACTS_PROFILE_MODULE', None)
CYCLOPE_CONTACTS_PROFILE_ADMIN_INLINE_MODULE = getattr(settings, 'CYCLOPE_CONTACTS_PROFILE_ADMIN_INLINE_MODULE', None)
CYCLOPE_CONTACTS_PROFILE_TEMPLATE = getattr(settings, 'CYCLOPE_CONTACTS_PROFILE_TEMPLATE', None)

# pagination
CYCLOPE_PAGINATION = getattr(settings, 'CYCLOPE_PAGINATION',
                             { 'TEASER' : 5,
                               'LABELED_ICON' : 30,
                               'FORUM' : 30,
                               'DETAIL' : 9999,
                               })
CYCLOPE_RSS_LIMIT = 50

# Feed

CYCLOPE_FEED_CACHE_TIME = getattr(settings, 'CYCLOPE_FEED_CACHE_TIME', 600)

CYCLOPE_PROJECT_PATH = getattr(settings, 'CYCLOPE_PROJECT_PATH', None)

if not CYCLOPE_PROJECT_PATH:
    raise ImproperlyConfigured(
        ugettext('You need to set the CYCLOPE_PROJECT_PATH in your settings file.'))
# we normalize the path
CYCLOPE_PROJECT_PATH = os.path.normpath(CYCLOPE_PROJECT_PATH)

CYCLOPE_PROJECT_NAME = os.path.basename(CYCLOPE_PROJECT_PATH)

#TODO(nicoechaniz): re-evaluate the way we are handling these dynamic settings, it is practical but seems hacky and error-prone.

sys.path.append(os.path.join(CYCLOPE_THEMES_ROOT, '../'))
import themes

CYCLOPE_BASE_CONTENT_TYPES = site.base_content_types

def get_site_settings():
    """Get the SiteSettings object.

    Returns:
        SiteSettings instance or None if no SiteSettings have been created.

    """
    from django.core.exceptions import ObjectDoesNotExist
    from django.db.utils import DatabaseError
    try:
        # a Cyclope project is supposed to have only one SiteSettings object
        #TODO(nicoechaniz): Fix for multi-site
        site_settings = SiteSettings.objects.get()

    # catch exceptions if the database is not available or no settings created
    except (DatabaseError, IndexError):
        site_settings = None

    return site_settings

def populate_from_site_settings(site_settings):
    # Read some settings and make them available at module level
    CYCLOPE_SITE_SETTINGS = site_settings
    CYCLOPE_BASE_URL = "http://" + CYCLOPE_SITE_SETTINGS.site.domain # FIXME: could be https
    CYCLOPE_CURRENT_THEME = CYCLOPE_SITE_SETTINGS.theme
    if CYCLOPE_CURRENT_THEME in themes.local_themes:
        CYCLOPE_THEME_MEDIA_URL = '%s%s/' % (
            settings.CYCLOPE_LOCAL_THEMES_MEDIA_PREFIX, CYCLOPE_CURRENT_THEME)
    else:
        CYCLOPE_THEME_MEDIA_URL = '%sthemes/%s/' % (CYCLOPE_STATIC_URL,
                                                    CYCLOPE_CURRENT_THEME)

    CYCLOPE_THEME_PREFIX = 'cyclope/themes/%s/' % CYCLOPE_CURRENT_THEME
    CYCLOPE_THEME_BASE_TEMPLATE = 'cyclope/themes/%s/base.html' \
                                   % CYCLOPE_CURRENT_THEME

    if CYCLOPE_SITE_SETTINGS.default_layout_id:
        try:
            CYCLOPE_DEFAULT_LAYOUT = CYCLOPE_SITE_SETTINGS.default_layout

            CYCLOPE_DEFAULT_TEMPLATE = 'cyclope/themes/%s/%s' % (
                CYCLOPE_CURRENT_THEME,
                CYCLOPE_DEFAULT_LAYOUT.template)

        #TODO(nicoechaniz): fix this workaround. It's here for migrations on the Layout model, which fail to complete with a DatabaseError when this module is imported. Eg: cyclope/migrations/0011...
        except DatabaseError:
            pass

    # Update the settings module with the settings
    for name, value in locals().copy().iteritems():
        if name.startswith("CYCLOPE"):
            globals()[name] = value

if hasattr(settings, "CYCLOPE_MULTISITE") and settings.CYCLOPE_MULTISITE:
    pass
else:
    CYCLOPE_SITE_SETTINGS = get_site_settings() # FIXME: This should be executed on
                                            # non multisite deploys
    populate_from_site_settings(CYCLOPE_SITE_SETTINGS)

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
    # (this deletes the relation, not the object)
    ctype = ContentType.objects.get_for_model(sender)
    if hasattr(instance, 'id'):
        related_from = RelatedContent.objects.filter(other_type=ctype,
                                                    other_id=instance.id)
        for obj in related_from:
            obj.delete()

def _delete_from_layouts_and_menuitems(sender, instance, **kwargs):
    # when a content is part of a layout or a menu_item we need to
    # clear this relation
    if instance.__class__ in site._registry:
        ctype = ContentType.objects.get_for_model(sender)

        RegionView = get_model('cyclope', 'regionview')
        RegionView.objects.filter(content_type=ctype, object_id=instance.id).delete()

        MenuItem = get_model('cyclope', 'menuitem')
        items = MenuItem.objects.filter(content_type=ctype, object_id=instance.id)
        for item in items:
            item.content_type = item.object_id = item.content_object = None
            item.save()

def reload_settings(**kwargs):
    """Reload this module to refresh settings.

    This is used in multi-site configurations."""

    reload(themes)
    reload(sys.modules[__name__])

pre_delete.connect(_delete_related_contents)
pre_delete.connect(_delete_from_layouts_and_menuitems)
