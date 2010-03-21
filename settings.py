"""Sets the default and automatic settings.

All settings will be available to templates if the site_settings context processor is installed.

Attributes:

  Overideable by the project settings.py:

    CYCLOPE_PREFIX: prefix for cyclope URLs, defaults to 'cyclope/'
    CYCLOPE_MEDIA_URL: URL to cyclope media files
    CYCLOPE_MEDIA_ROOT: defaults to cyclope/ folder of the project's MEDIA_ROOT
    CYCLOPE_THEMES_ROOT: path to the themes package

  Automatic (cannot be overriden):

    CYCLOPE_THEMES: the themes package
    CYCLOPE_SITE_SETTINGS: the SiteSettings instance
    CYCLOPE_CURRENT_THEME
    CYCLOPE_THEME_MEDIA_URL
    CYCLOPE_DEFAULT_LAYOUT
    CYCLOPE_DEFAULT_TEMPLATE
"""

from django.conf import settings
from django.utils.translation import ugettext as _
from utils import themes
import sys, os
from django.db.models.signals import post_save
from cyclope.models import SiteSettings

CYCLOPE_PREFIX = getattr(settings, 'CYCLOPE_ROOT_URL', \
                           'cyclope/')
CYCLOPE_MEDIA_URL = getattr(settings, 'CYCLOPE_MEDIA_URL', \
                           '%scyclope/' % settings.MEDIA_URL)
CYCLOPE_MEDIA_ROOT = getattr(settings, 'CYCLOPE_MEDIA_ROOT', \
                            '%scyclope/' % settings.MEDIA_ROOT)
CYCLOPE_THEMES_ROOT = getattr(settings, 'CYCLOPE_THEMES_ROOT',
                              os.path.join(os.path.dirname(__file__),
                                           "templates/cyclope/themes/"))

#TODO(nicoechaniz): re-evaluate the way we are handling these dynamic settings, it is practical but seems hacky and error-prone.

sys.path.append(os.path.join(CYCLOPE_THEMES_ROOT, '../'))
import themes as CYCLOPE_THEMES

#TODO(nicoechaniz): adapt for multi-site.
def get_site_settings():
    """Get the SiteSettings object.

    Returns:
        SiteSettings instance or None if no SiteSettings have been created.

    """
    from django.core.exceptions import ObjectDoesNotExist

    try:
        site_settings = SiteSettings.objects.get()
    except ObjectDoesNotExist:
        site_settings = None

    return site_settings

CYCLOPE_SITE_SETTINGS = get_site_settings()

# If the site has already been set up we read some settings
# and make them available at module level
if CYCLOPE_SITE_SETTINGS:
    CYCLOPE_CURRENT_THEME = CYCLOPE_SITE_SETTINGS.theme
    CYCLOPE_THEME_MEDIA_URL = '%sthemes/%s/' % (CYCLOPE_MEDIA_URL,
                                                CYCLOPE_CURRENT_THEME)
    CYCLOPE_DEFAULT_LAYOUT = CYCLOPE_SITE_SETTINGS.default_layout

    if CYCLOPE_DEFAULT_LAYOUT is not None:
        CYCLOPE_DEFAULT_TEMPLATE = '%sthemes/%s/%s' % (
            CYCLOPE_PREFIX, CYCLOPE_CURRENT_THEME,
            CYCLOPE_DEFAULT_LAYOUT.template)


def _refresh_site_settings(sender, instance, created, **kwargs):
    "Callback to refresh site settings when they are modified in the database"
    global CYCLOPE_SITE_SETTINGS
    CYCLOPE_SITE_SETTINGS = instance

post_save.connect(_refresh_site_settings, sender=SiteSettings)
