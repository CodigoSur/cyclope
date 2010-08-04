#!/usr/bin/env python

from cyclope.default_settings import *
import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

BASE_DIR = os.path.dirname(__file__)

INTERNAL_IPS = ('127.0.0.1',)

ADMINS = (
    ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = os.path.join(BASE_DIR, 'db/site.db')

TIME_ZONE = 'America/Argentina/Buenos_Aires'

SITE_ID = 1

USE_I18N = True

# Absolute path to the directory that holds media.
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
#MEDIA_ROOT = '/var/www/pyclope.nicoechaniz.com.ar/htdocs/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/admin/'

ROOT_URLCONF = 'cyclope_project.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates".
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, 'templates'),
)

#FILEBROWSER_MAX_UPLOAD_SIZE = 1048576 # 10 MB

LOGIN_REDIRECT_URL = '/inicio'

# cyclope settings
CYCLOPE_PREFIX = ''

#CYCLOPE_LOCAL_THEMES_DIR = os.path.join(BASE_DIR, 'templates/cyclope/themes/')
#CYCLOPE_LOCAL_THEMES_MEDIA_PREFIX = '/media/local_themes/'

HAYSTACK_WHOOSH_PATH = os.path.join(BASE_DIR, 'cyclope_project_index')

# import local settings if they are present
try:
    from local_settings import *
except:
    pass
