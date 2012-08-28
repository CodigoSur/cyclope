#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010-2012 Código Sur Sociedad Civil
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

"""This file holds default values related to settings that need to change when
a new app is installed.
"""

import os
import imp
ugettext = lambda s: s

#workaround for PIL when importing Image using different methods.
# see http://jaredforsyth.com/blog/2010/apr/28/accessinit-hash-collision-3-both-1-and-1/
# and https://sourceforge.net/tracker/?func=detail&atid=422030&aid=2993756&group_id=38414
import sys
import PIL.Image
sys.modules['Image'] = PIL.Image

SITE_ID = 1
USE_I18N = True
USE_L10N = True

## LANGUAGE_CODE = 'en'
LANGUAGES = (
    ('es', u'Español'),
    ('en', u'English'),
    ('pt', u'Português'),
    ('it', u'Italiano'),
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
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
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'cyclope.middleware.LayoutMiddleware',
#    'debug_toolbar.middleware.DebugToolbarMiddleware',

)

# the order of the INSTALLED_APPS is relevant to get the template load order right
INSTALLED_APPS = [
    'dbgettext',
    'rosetta',
    'haystack',
    'tagging',
    'tagging_autocomplete',


    'cyclope',
    'cyclope.core.collections',
    'cyclope.core.perms',
    'cyclope.apps.articles',
    'cyclope.apps.staticpages',
    'cyclope.apps.medialibrary',
    'cyclope.apps.polls',
    'cyclope.apps.forum',
    'cyclope.apps.newsletter',
    'cyclope.apps.contacts',
    'cyclope.apps.locations',
    'cyclope.apps.feeds',
    'cyclope.apps.dynamicforms',
    'cyclope.apps.abuse',
    'cyclope.apps.related_admin',
    'cyclope.apps.custom_comments',

    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',

    'threadedcomments',

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.humanize',
    'django.contrib.admin',
    'django.contrib.comments',
    'django.contrib.markup',
    'django.contrib.messages',
    'django.contrib.sitemaps',

    'autoslug',
    'feincms',
    'mptt',
    'captcha',
    'filebrowser',
    'south',
    'registration',
    'profiles',
    'contact_form',
    'markitup',
    'forms_builder.forms',

#    'debug_toolbar',
#    'django_extensions',
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'cyclope.core.perms.backends.CategoryPermBackend',
)


MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

# debug_toolbar settings
#DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS': False}

# comments settings
COMMENTS_APP = 'cyclope.apps.custom_comments'

# captcha settings
CAPTCHA_NOISE_FUNCTIONS=('captcha.helpers.noise_arcs',)
CAPTCHA_FONT_SIZE=30
CAPTCHA_LETTER_ROTATION=(-15,15)

# feincms settings
FEINCMS_ADMIN_MEDIA = '/media/feincms/'
# TreeEditor throws an exception in the admin for Category (as of 2010-02-19)
# if this is set to True
FEINCMS_TREE_EDITOR_INCLUDE_ANCESTORS = False

# filebrowser settings
FILEBROWSER_DEBUG = False
FILEBROWSER_DIRECTORY = 'uploads/'
FILEBROWSER_EXTENSIONS = {
    'Folder': [''],
    'Image': ['.jpg','.jpeg','.gif','.png','.tif','.tiff'],
    'Video': ['.ogv', '.ogg', '.mov','.wmv','.mpeg','.mpg','.avi','.rm', '.flv',],
    'Document': ['.odt', 'docx', '.pdf','.doc','.rtf','.txt',
                 '.ods', '.xls', '.xlsx', '.csv', '.ppt', '.pptx'],
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
    'fb_thumb': {'verbose_name': ugettext('Admin Thumbnail'),
                 'width': 60, 'height': 60, 'opts': 'crop upscale'},
    'thumbnail': {'verbose_name': ugettext('Thumbnail (100px height)'),
                  'width': '', 'height': 100, 'opts': ''},
    'small': {'verbose_name': ugettext('Small (300x300px)'),
              'width': 300, 'height': 300, 'opts': 'crop'},
    'medium': {'verbose_name': ugettext('Medium (460px width)'),
               'width': 460, 'height': '', 'opts': ''},
    'big': {'verbose_name': ugettext('Big (620px width)'),
            'width': 620, 'height': '', 'opts': ''},
    'cropped': {'verbose_name': ugettext('Cropped (60x60px)'),
                'width': 60, 'height': 60, 'opts': 'crop'},
    'croppedthumbnail': {'verbose_name': ugettext('Cropped Thumbnail (140x140px)'),
                         'width': 140, 'height': 140, 'opts': 'crop'},
    'slideshow': {'verbose_name': ugettext('Slideshow'),
                  'width': 300, 'height': 300, 'opts': 'crop'},
    'slideshow-background': {'verbose_name': ugettext('Slideshow'),
                  'width': 550, 'height': '', 'opts': 'crop'},
}

FILEBROWSER_MAX_UPLOAD_SIZE = 1024*1024*20 # 20MB

# django-registration settings
ACCOUNT_ACTIVATION_DAYS = 7

# profile settings
AUTH_PROFILE_MODULE = "cyclope.userprofile"

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

# dbgettext options
#DBGETTEXT_PROJECT_OPTIONS = 'cyclope.dbgettext_options'
DBGETTEXT_SPLIT_SENTENCES = False
DBGETTEXT_INLINE_HTML_TAGS = ('b','i','u','em','strong',)

# rosetta settings
ROSETTA_MESSAGES_SOURCE_LANGUAGE_CODE = 'es'
#ROSETTA_MAIN_LANGUAGE = 'es'
ROSETTA_MESSAGES_PER_PAGE = 15
ROSETTA_EXCLUDED_APPLICATIONS = (
    'admin_tools',
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
    'haystack',
    'dbgettext',
    'rosetta',
    )

# martkitup settings
JQUERY_URL = "cyclope/js/reuse_django_jquery.js" # We dont want jquery to be included twice in the admin.
MARKITUP_SET = 'cyclope/markitup/sets/textile'
MARKITUP_FILTER = ('django.contrib.markup.templatetags.markup.textile', {})

