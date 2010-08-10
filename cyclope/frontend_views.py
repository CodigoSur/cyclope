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

"""
cyclope.frontend_views
----------------------
"""

from django.utils.translation import ugettext_lazy as _
from django.template import loader, RequestContext
from django.contrib.sites.models import Site

from cyclope import settings as cyc_settings
from cyclope.core import frontend
from cyclope.models import Menu, MenuItem
from cyclope import views

#class SiteBreadcrumb(frontend.FrontendView):
#    """Navigation breadcrumb
#    """
#    name='breadcrumb'
#    verbose_name=_('navigation breadcrumb')
#    is_default = True
#    is_instance_view = False
#
#    def get_string_response(self, request, content_object=None, *args, **kwargs):
#        pass
#
#frontend.site.register_view(Site, SiteBreadcrumb())


class MenuRootItemsList(frontend.FrontendView):
    """A list view of the root MenuItems for a given Menu.
    """
    name='root_items_list'
    verbose_name=_('list of root items for the selected Menu')
    is_default = True

    def get_string_response(self, request, content_object=None, *args, **kwargs):
        menu_items = MenuItem.tree.filter(menu=content_object, level=0, active=True)
        c = RequestContext(request, {'menu_items': menu_items})
        t = loader.get_template("cyclope/menu_flat_items_list.html")
        c['host_template'] = 'cyclope/inline_view.html'
        return t.render(c)

frontend.site.register_view(Menu, MenuRootItemsList())


class MenuFlatItemsList(frontend.FrontendView):
    """A flat list view of all the MenuItems for a given Menu.
    """
    name='flat_items_list'
    verbose_name=_('flat list of all items for the selected Menu')

    def get_string_response(self, request, content_object=None, *args, **kwargs):
        menu_items = MenuItem.tree.filter(menu=content_object, active=True)
        c = RequestContext(request, {'menu_items': menu_items})
        t = loader.get_template("cyclope/menu_flat_items_list.html")
        c['host_template'] = 'cyclope/inline_view.html'
        return t.render(c)

frontend.site.register_view(Menu, MenuFlatItemsList())


#class MenuHierarchicalItemsList(frontend.FrontendView):
#    """A hierarchical list view of all the MenuItems for a given Menu.
#    """
#    name='hierarchical_items_list'
#    verbose_name=_('hierarchical list of all items for the selected Menu')
#
#    def get_string_response(self, request, content_object=None, *args, **kwargs):
#        menu_items = MenuItem.tree.filter(menu=content_object, active=True)
#        c = RequestContext(request, {'menu_items': menu_items})
#        t = loader.get_template("cyclope/menu_flat_items_list.html")
#        c['host_template'] = 'cyclope/inline_view.html'
#        return t.render(c)
#
#frontend.site.register_view(Menu, MenuFlatItemsList())


class MenuItemDescendantsOfCurrentItem(frontend.FrontendView):
    """List view of all the sub-items for the currently selected MenuItem
    """
    name='subitems_list'
    verbose_name=_('list view of sub-items for the selected menu item')
    is_default = True
    is_instance_view = False

    def get_string_response(self, request, *args, **kwargs):
        is_instance_view = False
        current_url = request.path_info[1:]
        menu_items = MenuItem.tree.get(url=current_url).get_descendants()
        c = RequestContext(request, {'menu_items': menu_items})
        t = loader.get_template("cyclope/menu_flat_items_list.html")
        c['host_template'] = 'cyclope/inline_view.html'
        return t.render(c)

frontend.site.register_view(MenuItem, MenuItemDescendantsOfCurrentItem())

#############
