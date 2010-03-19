from django.conf import settings
from django.utils.translation import ugettext as _
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

def get_site_settings():
    from cyclope.models import SiteSettings
    #ToDo: Return appropriate exceptions. Adapt for multi-site.
    # we are asuming there's only one site but this should be modified
    # to take the request url into account if we start using the
    # sites framework and make cyclope multi-site
    try:
        site_settings = SiteSettings.objects.get()
    except:
        site_settings = None
#        raise Exception(_(u'You need to create your site settings.'))
    return site_settings
CYCLOPE_SITE_SETTINGS = get_site_settings()

#If the site has already been set up...
if CYCLOPE_SITE_SETTINGS:
    def get_current_theme():
        try:
            current_theme = CYCLOPE_SITE_SETTINGS.theme
        except:
            raise Exception(
                    _(u'Improperly configured site. No theme selected.'))
        return current_theme
    CYCLOPE_CURRENT_THEME = get_current_theme()

    def get_theme_media_url():
        return '%sthemes/%s/' % (CYCLOPE_MEDIA_URL, CYCLOPE_CURRENT_THEME)
    CYCLOPE_THEME_MEDIA_URL = get_theme_media_url()

    def get_default_layout():
        return CYCLOPE_SITE_SETTINGS.default_layout
    CYCLOPE_DEFAULT_LAYOUT = get_default_layout()

    def get_default_template():
       return '%sthemes/%s/%s' % (CYCLOPE_PREFIX,
                                  CYCLOPE_CURRENT_THEME,
                                  CYCLOPE_DEFAULT_LAYOUT.template
                                  )
    CYCLOPE_DEFAULT_TEMPLATE = get_default_template()
