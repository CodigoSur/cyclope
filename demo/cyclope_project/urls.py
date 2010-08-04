#!/usr/bin/env python

from django.conf.urls.defaults import *
from cyclope import settings as cyc_settings
from cyclope.core import frontend
frontend.autodiscover()

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    (r'', include('cyclope.default_urls')),
    (r'^%s' % cyc_settings.CYCLOPE_PREFIX,
     include(frontend.site.get_urls())),
)
