from django.conf import settings
from utils import themes
import sys, os


#CYCLOPE_ROOT_URL = getattr(settings, 'CYCLOPE_ROOT_URL', \
#                           'cyclope/')

CYCLOPE_MEDIA_URL = getattr(settings, 'CYCLOPE_MEDIA_URL', \
                           '%scyclope/' % settings.MEDIA_URL)
CYCLOPE_MEDIA_ROOT = getattr(settings, 'CYCLOPE_MEDIA_ROOT', \
                            '%scyclope/' % settings.MEDIA_ROOT)

# this should not be hardcoded here, as the theme is now selectable from the SiteSettings admin
CYCLOPE_THEME = getattr(settings, 'CYCLOPE_THEME', 'potente')
CYCLOPE_THEME_MEDIA_URL = '%sthemes/%s/' % (CYCLOPE_MEDIA_URL, CYCLOPE_THEME)
CYCLOPE_THEME_MEDIA_ROOT = '%sthemes/%s/' % (CYCLOPE_MEDIA_ROOT, CYCLOPE_THEME)


CYCLOPE_THEMES_ROOT = getattr(settings, 'CYCLOPE_THEMES_ROOT',
                              os.path.join(os.path.dirname(__file__),
                                           "templates/cyclope/themes/"))

sys.path.append(os.path.join(CYCLOPE_THEMES_ROOT, '../'))
import themes as CYCLOPE_THEMES

