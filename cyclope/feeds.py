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

from django.contrib.syndication.views import Feed
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.core.urlresolvers import reverse
from cyclope.core.collections.models import Category
from cyclope.models import SiteSettings
import cyclope.settings as cyc_settings
import cyclope.core.frontend.sites as sites

class WholeSiteFeed(Feed):

    description_template = 'feeds/description.html'

    def title(self, obj):
        return cyc_settings.CYCLOPE_SITE_SETTINGS.global_title

    # TODO(diegoM): It would be better show the first paragraph?
    def item_description(self, content):
        if hasattr(content, 'text'):
            return content.text
        elif hasattr(content, 'description'):
            return content.description

    def item_author(self, content):
        return content.author.name

    def link(self):
        return reverse('whole_site_feed')

    def item_title(self, item):
        #FIXME(diegoM): How to get the right translation of the object_name ?
        return "%s  (%s)" % (item.name, item.get_verbose_name().capitalize())

    def items(self):
        N = cyc_settings.CYCLOPE_RSS_LIMIT
        objs = []
        for ctype in SiteSettings.objects.get().rss_content_types.all():
            objs.extend(list(ctype.model_class().objects.filter(published=True)[:N]))
        return sorted(objs, key=lambda x: x.creation_date, reverse = True)[:N]

class ContentTypeFeed(WholeSiteFeed):

    def title(self, obj):
        return u'%s | %s' % (cyc_settings.CYCLOPE_SITE_SETTINGS.global_title,
                             obj._meta.verbose_name_plural.capitalize())

    def get_object(self, request, object_name):
        for model in sites.site.base_content_types:
            if model.get_object_name() == object_name:
                return model
        raise Http404

    def link(self, model):
        return reverse('content_type_feed', args=[model.get_object_name()])

    def items(self, model):
        N = cyc_settings.CYCLOPE_RSS_LIMIT
        return model.objects.filter(published=True).order_by('-creation_date')[:N]

class CategoryFeed(WholeSiteFeed):

    def title(self, obj):
        return u'%s | %s' % (cyc_settings.CYCLOPE_SITE_SETTINGS.global_title,
                             obj.name.capitalize())

    def get_object(self, request, slug):
        return get_object_or_404(Category, slug=slug)

    def link(self, category):
        return reverse('category_feed', args=[category.slug])

    def items(self, category):
        N = cyc_settings.CYCLOPE_RSS_LIMIT
        objs = []
        for c in category.categorizations.all():
            if c.content_object.published:
              objs.append(c.content_object)
        return sorted(objs, key=lambda x: x.creation_date, reverse = True)[:N]
