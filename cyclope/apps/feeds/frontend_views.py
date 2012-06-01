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

from datetime import datetime
from django import forms
from django.utils.translation import ugettext_lazy as _

from cyclope.core import frontend
from cyclope import views
from cyclope import settings as cyc_settings
import feedparser

from models import Feed

# timedelta.total_seconds is new in python 2.7 http://docs.python.org/library/datetime.html
# so we define an equivalent here for compatibility's sake
def total_seconds(td):
    return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 10**6


class FeedDetailOptions(forms.Form):
    limit_to_n_items = forms.IntegerField(label=_('entries to show'), required=False)
    titles_only = forms.BooleanField(label=_('show titles only'), initial=False, required=False)

class FeedDetail(frontend.FrontendView):
    """Detail view for Feeds"""
    name='detail'
    verbose_name=_('detailed view of the selected Feed')
    is_default = True
    is_instance_view = True
    is_content_view = True
    is_region_view = True
    options_form = FeedDetailOptions

    _feed_cache = {}

    def get_response(self, request, req_context, options, content_object):
        if not options['limit_to_n_items']:
            options['limit_to_n_items'] = content_object.number_of_entries
        if not options['titles_only']:
            options['titles_only'] = content_object.titles_only

        now = datetime.now()
        d, last_access = self._feed_cache.get(content_object.url, (None, None))
        if d is None or total_seconds(now - last_access) > cyc_settings.CYCLOPE_FEED_CACHE_TIME:
            d = feedparser.parse(content_object.url)
            self._feed_cache[content_object.url] = (d, now)
        context = {'entries': d.entries[:options['limit_to_n_items']]}
        return views.object_detail(request, req_context, content_object,
                                   extra_context=context)

frontend.site.register_view(Feed, FeedDetail)

