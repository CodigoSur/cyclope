#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010 Código Sur - Nuestra América Asoc. Civil / Fundación Pacificar.
# All rights reserved.
#
# This file is part of Cyclope.
#
# Cyclope is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Cyclope is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# urls should be set at project level using cyclope.site.autodiscover()
# to populate cyclope.site.urls

# see cyclope_demo for an example

#!/usr/bin/env python

from django.conf.urls.defaults import *
from django.conf import settings as django_settings
from django.utils.translation import ugettext as _
from django.contrib import admin
from registration.views import register
from haystack.views import SearchView, search_view_factory
from cyclope.forms import UserProfileForm
from cyclope.core.captcha_contact_form.forms import  \
                                       AdminSettingsContactFormWithCaptcha
import cyclope.settings as cyc_settings
from cyclope.feeds import CategoryFeed, WholeSiteFeed, ContentTypeFeed

urlpatterns = patterns('',
    (r'^admin/filebrowser/', include('filebrowser.urls')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    url(r'^admin_tools/', include('admin_tools.urls')),
    (r'^i18n/', include('django.conf.urls.i18n')),

    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^captcha/', include('captcha.urls')),
    (r'^tagging_autocomplete/', include('tagging_autocomplete.urls')),
    url(r'^accounts/register/$', 'registration.views.register',
        {'backend': 'cyclope.registration_backends.CaptchaBackend'},
        name='registration_register'),
    (r'^accounts/', include('registration.backends.default.urls')),
    (r'^profiles/create/$', 'profiles.views.create_profile',
     {'form_class': UserProfileForm}),
    (r'^profiles/edit/$', 'profiles.views.edit_profile',
     {'form_class': UserProfileForm}),

    (r'^profiles/', include('profiles.urls')),

    url(r'^contact/$', 'contact_form.views.contact_form',
        {'form_class': AdminSettingsContactFormWithCaptcha},
        name='contact_form'),
    (r'^contact/', include('contact_form.urls')),
    url(r'^search/', search_view_factory(
        view_class=SearchView,
        results_per_page=cyc_settings.CYCLOPE_PAGINATION['TEASER']),
        name='haystack_search'),
    url(r'^rss/category/(?P<slug>[\w-]+)/$', CategoryFeed(),
        name='category_feed'),
    url(r'^rss/$', WholeSiteFeed(),
        name='whole_site_feed'),
    url(r'^rss/(?P<object_name>[\w-]+)/$', ContentTypeFeed(),
        name='content_type_feed'),
    (r'^newsletter/', include('cyclope.apps.newsletter.urls')),
    url(r'^markitup/', include('markitup.urls')),
    (r'^locations/', include('cyclope.apps.locations.urls')),
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
        ## url(r'^rosetta/translate/(?P<langid>[\w\-]+)/(?P<idx>\d+)/',
        ##     'cyclope.helper_views.rosetta_select_and_translate'),
        url(r'^rosetta/', include('rosetta.urls')),
    )

    urlpatterns += patterns('',
        url(r'^accounts/login/$', 'django.contrib.auth.views.login',
            {'template_name': 'admin/login.html'}),
    )
