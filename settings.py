from django.conf import settings
from utils import themes
import sys, os


CYCLOPE_PREFIX = getattr(settings, 'CYCLOPE_ROOT_URL', \
                           'cyclope/')

CYCLOPE_MEDIA_URL = getattr(settings, 'CYCLOPE_MEDIA_URL', \
                           '%scyclope/' % settings.MEDIA_URL)
CYCLOPE_MEDIA_ROOT = getattr(settings, 'CYCLOPE_MEDIA_ROOT', \
                            '%scyclope/' % settings.MEDIA_ROOT)
CYCLOPE_THEMES_ROOT = getattr(settings, 'CYCLOPE_THEMES_ROOT',
                              os.path.join(os.path.dirname(__file__),
                                           "templates/cyclope/themes/"))

#ToDo: is this too hacky?
sys.path.append(os.path.join(CYCLOPE_THEMES_ROOT, '../'))
import themes as CYCLOPE_THEMES

