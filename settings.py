from django.conf import settings

CYCLOPE_ROOT_URL = getattr(settings, 'CYCLOPE_ROOT_URL', \
                           'cyclope/')
#                           'cyclope/' % settings.MEDIA_URL)

CYCLOPE_MEDIA_URL = getattr(settings, 'CYCLOPE_MEDIA_URL', \
                           '%scyclope/' % settings.MEDIA_URL)
CYCLOPE_MEDIA_ROOT = getattr(settings, 'CYCLOPE_MEDIA_ROOT', \
                            '%scyclope/' % settings.MEDIA_ROOT)

CYCLOPE_THEME = getattr(settings, 'CYCLOPE_THEME', 'potente')
CYCLOPE_THEME_MEDIA_URL = '%s/themes/%s/' % (CYCLOPE_MEDIA_URL, CYCLOPE_THEME)
CYCLOPE_THEME_MEDIA_ROOT = '%s/themes/%s/' % (CYCLOPE_MEDIA_ROOT, CYCLOPE_THEME)

#CYCLOPE_THEME_MEDIA_PREFIX = getattr(settings, 'CYCLOPE_MEDIA_PREFIX',
#                               '/media/cyclope/themes/%s/' \
#                               % CYCLOPE_THEME)
