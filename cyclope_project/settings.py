#!/usr/bin/env python

import os
gettext = lambda s: s

#workaround for PIL when importing Image using different methods.
# see http://jaredforsyth.com/blog/2010/apr/28/accessinit-hash-collision-3-both-1-and-1/
# and https://sourceforge.net/tracker/?func=detail&atid=422030&aid=2993756&group_id=38414
import sys
import PIL.Image
sys.modules['Image'] = PIL.Image

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

ROOT_URLCONF = 'cyclope_project.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates".
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, 'templates'),
)

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
    'contact_form'
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
LOGIN_REDIRECT_URL = '/inicio'

# profile settings
AUTH_PROFILE_MODULE = "cyclope.userprofile"

# cyclope settings
CYCLOPE_PREFIX = ''
#CYCLOPE_LOCAL_THEMES_DIR = os.path.join(BASE_DIR, 'templates/cyclope/themes/')
#CYCLOPE_LOCAL_THEMES_MEDIA_PREFIX = '/media/local_themes/'

# tagging settings
FORCE_LOWERCASE_TAGS = True

# admin-toolls settings

ADMIN_TOOLS_INDEX_DASHBOARD = 'cyclope.dashboard.CustomIndexDashboard'
ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'cyclope.dashboard.CustomAppIndexDashboard'
ADMIN_TOOLS_THEMING_CSS = 'cyclope/css/admin_tools_theming.css'


# import local settings if they are present
try:
    from local_settings import *
except:
    pass
