#!/usr/bin/env python

import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

INTERNAL_IPS = ('127.0.0.1',)

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = os.path.join(os.path.dirname(__file__), 'example.db')

TIME_ZONE = 'America/Argentina/Buenos_Aires'

LANGUAGE_CODE = 'es'

SITE_ID = 1

USE_I18N = True

# Absolute path to the directory that holds media.
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'media/')
#MEDIA_ROOT = '/var/www/pyclope.nicoechaniz.com.ar/htdocs/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/admin/'


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
    "django.core.context_processors.request",
    "cyclope.core.context_processors.site_settings"
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

ROOT_URLCONF = 'cyclope_demo.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates".
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.comments',
#    'django.contrib.humanize',
#    'django.contrib.databrowse',
    'django.contrib.admin',

#    'tagging',
#   'rosetta'
    'autoslug',
    'feincms',
    'mptt',

#    'south',
#    'ajax_filtered_fields',
#    'debug_toolbar',

    'cyclope',
    'cyclope.core.collections',
#    'cyclope.apps.articles',

)

# make sure you point this to your Feincms media files.
FEINCMS_ADMIN_MEDIA = MEDIA_URL + 'feincms/'
# TreeEditor throws an exception in the admin for Category (as of 2010-02-19)
# if this is set to True
FEINCMS_TREE_EDITOR_INCLUDE_ANCESTORS = False
