# -*- coding: utf-8 -*-

from copy import copy
from django import template
from cyclope import settings as cyc_settings
from cyclope.models import MenuItem, RegionView
from cyclope.utils import layout_for_request
from cyclope.core import frontend

register = template.Library()

@register.inclusion_tag('cyclope/region.html', takes_context=True)
def region(context, region_name):
    """A region where views can be inserted in a template.

    The views that will actualy be inserted are defined in a Layout.

    Usage::

        {% region 'region_name' %}

    The region name should be one of the regions available to the template
    according to the theme configuration (check the theme's __init__ file)

    """

    # content should be a normal block, not a region.
    if region_name == 'content':
        return {}

    layout = layout_for_request(context['request'])
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
        if regionview.content_object:
            slug = regionview.content_object.slug
        else:
            slug=None

#        view_vars['output'] = view(context['request'], inline=True, slug=slug)
        view_vars['output'] = view(context['request'], slug=slug)
        view_vars['name'] = regionview.content_view
        views.append(view_vars)

    region_vars['views'] = views

    return region_vars
