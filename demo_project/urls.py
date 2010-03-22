#!/usr/bin/env python

from django.conf.urls.defaults import *
from django.conf import settings as django_settings
from django.utils.translation import ugettext as _
from django.conf import settings as django_settings

# cyclope.autodiscover will search inside installed apps folders
# for frontend.py files and register the views/urls declared.
import cyclope
cyclope.autodiscover()

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    (r'^admin/', include(admin.site.urls)),
    (r'^%s' % cyclope.settings.CYCLOPE_PREFIX, include(cyclope.site.urls)),
)

if django_settings.DEBUG:
    urlpatterns+= patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': django_settings.MEDIA_ROOT, 'show_indexes': True})
    )

if 'rosetta' in django_settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^rosetta/', include('rosetta.urls')),
    )

    urlpatterns += patterns('',
        url(r'^accounts/login/$', 'django.contrib.auth.views.login',
            {'template_name': 'admin/login.html'}),
    )
