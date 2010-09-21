#!/usr/bin/env python
# -*- coding: UTF-8 -*-
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

from django.contrib.syndication.views import Feed, FeedDoesNotExist
from django.shortcuts import get_object_or_404
from cyclope.core.collections.models import Category
from cyclope.models import BaseContent
import cyclope.settings as cyc_settings

class CategoryFeed(Feed):

    def get_object(self, request, slug):
        return get_object_or_404(Category, slug=slug)

    def link(self, category):
        return category.get_absolute_url()

    # TODO(diegoM): It would be better show the first paragraph?
    def item_description(self, content):
        return getattr(content, 'pretitle', '')

    def item_author(self, content):
        return content.author.name

    def items(self, category):
        N = cyc_settings.CYCLOPE_RSS_LIMIT
        # TODO(nicoechaniz):this hardcoded order_by is wrong. fix it.
        return [c.content_object for c in
                category.categorizations.order_by('-article__date')[:N]]
