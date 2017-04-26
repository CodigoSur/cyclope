#!/usr/bin/env python

from django.conf.urls import patterns, include, url
import haystack # This is here preventing a circular import
from cyclope import settings as cyc_settings
from cyclope.core import frontend
frontend.autodiscover()

from django.contrib import admin
admin.autodiscover()

handler500 = 'cyclope.views.error_500'
handler404 = 'cyclope.views.error_404'

urlpatterns = patterns('',
    (r'', include('cyclope.default_urls')),
    (r'^%s' % cyc_settings.CYCLOPE_PREFIX,
     include(frontend.site.get_urls())),
)
