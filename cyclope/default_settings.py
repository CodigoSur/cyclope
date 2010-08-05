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

import os
gettext = lambda s: s

#workaround for PIL when importing Image using different methods.
# see http://jaredforsyth.com/blog/2010/apr/28/accessinit-hash-collision-3-both-1-and-1/
# and https://sourceforge.net/tracker/?func=detail&atid=422030&aid=2993756&group_id=38414
import sys
import PIL.Image
sys.modules['Image'] = PIL.Image


# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
    'django.template.loaders.eggs.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
    "cyclope.core.context_processors.site_settings",
)


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.csrf.CsrfResponseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.doc.XViewMiddleware',
#    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

#DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS': False}



INSTALLED_APPS = (
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.humanize',
    'django.contrib.databrowse',
    'django.contrib.admin',
    'django.contrib.comments',

    'tagging',
    'tagging_autocomplete',
    'autoslug',
    'feincms',
    'mptt',
    'captcha',
    'filebrowser',
    'south',
    'registration',
    'profiles',

#    'debug_toolbar',

    'cyclope',
    'cyclope.core.collections',
    'cyclope.core.captcha_comments',
    'cyclope.apps.articles',
    'cyclope.apps.staticpages',
    'cyclope.apps.medialibrary',
    'contact_form',
    'haystack',
)

# comments settings
COMMENTS_APP = 'cyclope.core.captcha_comments'

# captcha settings
CAPTCHA_NOISE_FUNCTIONS=('captcha.helpers.noise_arcs',)
CAPTCHA_FONT_SIZE=30
CAPTCHA_LETTER_ROTATION=(-15,15)

# feincms settings
FEINCMS_ADMIN_MEDIA = '/feincms_media/'
# TreeEditor throws an exception in the admin for Category (as of 2010-02-19)
# if this is set to True
FEINCMS_TREE_EDITOR_INCLUDE_ANCESTORS = False

# filebrowser settings
FILEBROWSER_DEBUG = False
FILEBROWSER_DIRECTORY = 'uploads/'
FILEBROWSER_EXTENSIONS = {
    'Folder': [''],
    'Image': ['.jpg','.jpeg','.gif','.png','.tif','.tiff'],
    'Video': ['.ogg', '.mov','.wmv','.mpeg','.mpg','.avi','.rm',],
    'Document': ['.odt', 'docx', '.pdf','.doc','.rtf','.txt',
                 '.ods', '.xls','.csv'],
    'Audio': ['.ogg', '.mp3','.mp4','.wav','.aiff','.midi','.m4p'],
    'Code': ['.html','.py','.js','.css'],
    'Flash_App': ['.swf',],
    'Flash_Movie': ['.flv',],
}

FILEBROWSER_SELECT_FORMATS = {
    'File': ['Folder','Document',],
    'Image': ['Image'],
    'Media': ['Video','Sound'],
    'Document': ['Document'],
    'Flash': ['Flash_App', 'Flash_Movie'],
    'Video': ['Video', 'Flash_Movie',],
    'Audio': ['Audio'],
    # for TinyMCE we also have to define lower-case items
    'image': ['Image'],
    'file': ['Folder','Image','Document',],
}

FILEBROWSER_VERSIONS = {
    'fb_thumb': {'verbose_name': gettext('Admin Thumbnail'),
                 'width': 60, 'height': 60, 'opts': 'crop upscale'},
    'thumbnail': {'verbose_name': gettext('Thumbnail (140px)'),
                  'width': 140, 'height': '', 'opts': ''},
    'small': {'verbose_name': gettext('Small (300px)'),
              'width': 300, 'height': 300, 'opts': 'crop'},
    'medium': {'verbose_name': gettext('Medium (460px)'),
               'width': 460, 'height': '', 'opts': ''},
    'big': {'verbose_name': gettext('Big (620px)'),
            'width': 620, 'height': '', 'opts': ''},
    'cropped': {'verbose_name': gettext('Cropped (60x60px)'),
                'width': 60, 'height': 60, 'opts': 'crop'},
    'croppedthumbnail': {'verbose_name': gettext('Cropped Thumbnail (140x140px)'),
                         'width': 140, 'height': 140, 'opts': 'crop'},
}

FILEBROWSER_MAX_UPLOAD_SIZE = 1048576

# django-registration settings
ACCOUNT_ACTIVATION_DAYS = 7

# profile settings
AUTH_PROFILE_MODULE = "cyclope.userprofile"

# cyclope settings
CYCLOPE_PREFIX = ''

# tagging settings
FORCE_LOWERCASE_TAGS = True

# admin-tools settings

ADMIN_TOOLS_INDEX_DASHBOARD = 'cyclope.dashboard.CustomIndexDashboard'
ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'cyclope.dashboard.CustomAppIndexDashboard'
ADMIN_TOOLS_THEMING_CSS = 'cyclope/css/admin_tools_theming.css'

LOCALE_PATHS = (os.path.join(os.path.dirname(__file__), "locale_external"), )

# django-haystack settings
HAYSTACK_SITECONF = 'cyclope_project.search_sites'
HAYSTACK_SEARCH_ENGINE = 'whoosh'
