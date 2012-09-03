#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2012 Código Sur - Nuestra América Asoc. Civil / Fundación Pacificar.
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

from django.contrib.sitemaps import Sitemap

from cyclope.models import MenuItem
from cyclope.core.collections.models import Collection, Category
import cyclope.settings as cyc_settings


class CategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.2

    def items(self):
        return Category.objects.filter(collection__visible = True)


class CollectionSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.3

    def items(self):
        return Collection.objects.filter(visible=True)


class MenuSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):

        menu_items = MenuItem.objects.filter(active=True).exclude(
                                                    custom_url__contains="http")
        return menu_items

    def location(self, obj):
        return obj.custom_url or cyc_settings.CYCLOPE_PREFIX + "/" + obj.url
