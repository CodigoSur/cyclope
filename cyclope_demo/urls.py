#!/usr/bin/env python

from django.conf.urls.defaults import *
from django.conf import settings as django_settings
from django.utils.translation import ugettext as _
from django.conf import settings as django_settings

from cyclope import settings as cyc_settings

# autodiscover will search inside installed apps folders
# for frontend_views.py files and register the views/urls declared.
from cyclope.core import frontend
frontend.autodiscover()

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/filebrowser/', include('filebrowser.urls')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    (r'^admin/', include(admin.site.urls)),
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^captcha/', include('captcha.urls')),
    (r'^tagging_autocomplete/', include('tagging_autocomplete.urls')),
    (r'^%s' % cyc_settings.CYCLOPE_PREFIX,
     include(frontend.site.get_urls())),
)

if django_settings.DEBUG:
    urlpatterns+= patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': django_settings.MEDIA_ROOT, 'show_indexes': True})
    )

    import os, feincms
    feincms_root = os.path.join(feincms.__path__[0], 'media/feincms/')
    urlpatterns+= patterns('',
        url(r'^feincms_media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': feincms_root, 'show_indexes': True})
    )


if 'rosetta' in django_settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^rosetta/', include('rosetta.urls')),
    )

    urlpatterns += patterns('',
        url(r'^accounts/login/$', 'django.contrib.auth.views.login',
            {'template_name': 'admin/login.html'}),
    )
