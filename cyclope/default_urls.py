#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010-2012 Código Sur Sociedad Civil
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

# see cyclope/demo for an example

from django.conf.urls import patterns, include, url
from django.conf import settings as django_settings
from django.contrib import admin
from haystack.views import SearchView, search_view_factory
from cyclope.core.captcha_contact_form.forms import  \
                                       AdminSettingsContactFormWithCaptcha
import cyclope.settings as cyc_settings
from cyclope.feeds import CategoryFeed, WholeSiteFeed, ContentTypeFeed
from cyclope.sitemaps import CategorySitemap, CollectionSitemap, MenuSitemap
from cyclope.core.user_profiles.forms import UserProfileForm

urlpatterns = patterns('',
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap',
        {'sitemaps': {"menus": MenuSitemap, "categories": CategorySitemap,
                      "collections": CollectionSitemap}}),
    url(r'^robots\.txt$', 'django.views.generic.simple.direct_to_template',
        {'template': 'cyclope/robots.txt', 'mimetype': 'text/plain'}),

    ## cyclope apps
    url(r'^locations/', include('cyclope.apps.locations.urls')),
    url(r'^newsletter/', include('cyclope.apps.newsletter.urls')),
    url(r'^abuse/', include('cyclope.apps.abuse.urls')),
    url(r'^related_admin/', include('cyclope.apps.related_admin.urls')),
    url(r'^rss/category/(?P<slug>[\w-]+)/$', CategoryFeed(), name='category_feed'),
    url(r'^rss/$', WholeSiteFeed(), name='whole_site_feed'),
    url(r'^rss/(?P<object_name>[\w-]+)/$', ContentTypeFeed(), name='content_type_feed'),
    url(r'^search/', search_view_factory(
        view_class=SearchView,
        results_per_page=cyc_settings.CYCLOPE_PAGINATION['TEASER']),
        name='haystack_search'),

    ## admin & django contrib
    url(r'^admin/filebrowser/', include('filebrowser.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^comments/', include('django.contrib.comments.urls')),

    ## 3rd party
    # captcha (django-simple-captcha)
    url(r'^captcha/', include('captcha.urls')),
    # accounts (django-registration)
    url(r'^accounts/register/$', 'registration.views.register',
        {'backend': 'cyclope.registration_backends.CaptchaBackend'},
        name='registration_register'),
    url(r'^accounts/', include('registration.backends.default.urls')),

    # profiles (cyclope.core.user_profiles & django-profiles)
    url(r'^profiles/me/$', 'cyclope.core.user_profiles.views.me'), # to redirect to the proper url of user_profiles
    url(r'^profiles/create/$', 'profiles.views.create_profile',
        {'form_class': UserProfileForm, "success_url": "/profiles/me/"},
        name="profiles_create_profile"),
    url(r'^profiles/edit/$', 'profiles.views.edit_profile',
        {'form_class': UserProfileForm, "success_url": "/profiles/me/"},
        name="profiles_edit_profile"),
    url(r'^profiles/(?P<username>\w+)/$', "profiles.views.profile_detail",
        name='profiles_profile_detail'),

    # contact (django-contact-form)
    url(r'^contact/$', 'contact_form.views.contact_form',
        {'form_class': AdminSettingsContactFormWithCaptcha},
        name='contact_form'),
    url(r'^contact/', include('contact_form.urls')),
    # markitup
    url(r'^markitup/', include('markitup.urls')),
    # custom-forms (django-forms-builder)
    url(r'^forms/', include("forms_builder.forms.urls")),
    # django-generic-ratings
    (r'^ratings/', include('ratings.urls')),
)

if django_settings.DEBUG:
    urlpatterns+= patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': django_settings.MEDIA_ROOT, 'show_indexes': True})
    )

if 'live' in django_settings.INSTALLED_APPS:
    urlpatterns += patterns('',
                            (r'^live/', include('live.urls')),
                            )

if 'schedule' in django_settings.INSTALLED_APPS:
    urlpatterns += patterns('',
                            (r'^schedule/', include('schedule.urls')),
                            )

if 'rosetta' in django_settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        ## url(r'^rosetta/translate/(?P<langid>[\w\-]+)/(?P<idx>\d+)/',
        ##     'cyclope.helper_views.rosetta_select_and_translate'),
        url(r'^rosetta/', include('rosetta.urls')),
    )
