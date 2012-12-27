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

"""
templatetags.layout
-------------------

Template tags to mark regions in a template, which enable the configuration
of different Layouts.
"""

from django import template
from cyclope.utils import layout_for_request, get_or_set_cache
from cyclope.core import frontend

register = template.Library()

@register.inclusion_tag('cyclope/region.html', takes_context=True)
def region(context, region_name):
    """Defines a region where views can be inserted in a template.

    The views that will actualy be inserted are defined in a Layout.

    Usage::

        {% region 'region_name' %}

    The region name must be one of the regions available to the template
    according to the theme configuration (as defined in the theme's __init__ file)

    """

    # if we have a layout in the context use that one, otherwise guess it from the request
    layout = context.get('layout', layout_for_request(context['request']))
    region_vars = {'layout_name': layout.slug, 'region_name': region_name}

    regionviews = layout.regionview_set.filter(
        region=region_name).order_by('weight')
    views = []


    for regionview in regionviews:
        view_vars={}
        view = frontend.site.get_view(
            regionview.content_type.model_class(),
            regionview.content_view,
            )
        # instance views need instance data -> slug
        if view.is_instance_view:
            if regionview.content_object is None:
                raise template.TemplateSyntaxError
            slug = regionview.content_object.slug
            view_vars['output'] = view(context['request'], region_name=region_name,
                                       content_object=regionview.content_object,
                                       view_options=regionview.view_options)
            view_vars['slug'] = slug
        else:
            view_vars['output'] = view(context['request'], region_name=region_name,
                                       view_options=regionview.view_options)
        view_vars['name'] = regionview.content_view
        view_vars['model'] = regionview.content_type.model
        views.append(view_vars)

    region_vars['views'] = views

    return region_vars
