#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django.conf.urls import include
from cyclope import settings as cyc_settings

# cyclope.autodiscover will search inside installed apps folders
# for frontend.py files and register the views/urls declared.
from cyclope.core import frontend
frontend.autodiscover()

urlpatterns = [
    (r'^%s' % cyc_settings.CYCLOPE_PREFIX, include(frontend.site.get_urls())),
]
