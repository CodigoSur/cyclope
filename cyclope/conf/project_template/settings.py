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

from cyclope.default_settings import *
import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

CYCLOPE_PROJECT_PATH = os.path.dirname(__file__)

INTERNAL_IPS = ('127.0.0.1',)

ADMINS = (
    ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = os.path.join(CYCLOPE_PROJECT_PATH, 'db/site.db')

TIME_ZONE = 'America/Argentina/Buenos_Aires'

# Absolute path to the directory that holds media.
MEDIA_ROOT = os.path.join(CYCLOPE_PROJECT_PATH, 'media/')
#MEDIA_ROOT = '/var/www/pyclope.nicoechaniz.com.ar/htdocs/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'
STATIC_URL = '/media/'

STATIC_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/admin/'

ROOT_URLCONF = '{{ project_name }}.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates".
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(CYCLOPE_PROJECT_PATH, 'templates'),
)

INSTALLED_APPS += (
    '{{ project_name }}',
)

#FILEBROWSER_MAX_UPLOAD_SIZE = 1048576 # 10 MB

LOGIN_REDIRECT_URL = '/inicio'


# cyclope settings

#CYCLOPE_LOCAL_THEMES_DIR = os.path.join(CYCLOPE_PROJECT_PATH, 'templates/cyclope/themes/')
#CYCLOPE_LOCAL_THEMES_MEDIA_PREFIX = '/media/local_themes/'

CYCLOPE_PREFIX = ''

#CYCLOPE_CONTACTS_PROFILE_MODULE = "app.model"
#CYCLOPE_CONTACTS_PROFILE_ADMIN_INLINE_MODULE = "project.app.admin.ProfileModuleInline"
#CYCLOPE_CONTACTS_PROFILE_TEMPLATE = "app/profile_template.html"

# possible values for TEXT_STYLE are:
# textile (saves markup, renders with corresponding filter)
# wysiwyg (rich text editor, saves HTML, renders with safe filter)
# raw (simple text area saves the raw input, renders with safe filter)

CYCLOPE_TEXT_STYLE = 'textile'

HAYSTACK_SITECONF = '{{ project_name }}.search_sites'
HAYSTACK_WHOOSH_PATH = os.path.join(CYCLOPE_PROJECT_PATH, 'cyclope_project_index')

# import local settings if they are present
try:
    from local_settings import *
except:
    pass
