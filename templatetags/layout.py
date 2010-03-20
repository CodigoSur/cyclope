from copy import copy
from django import template
from cyclope import settings as cyc_settings, site as cyc_site
from cyclope.models import MenuItem, RegionView
from cyclope.utils import layout_for_request

register = template.Library()

@register.inclusion_tag('cyclope/region.html', takes_context=True)
def region(context, region_name):

    # content should be a normal block, not a region.
    if region_name == 'content':
        return {}

    layout = layout_for_request(context['request'])
    region_vars = {'layout_name': layout.slug, 'region_name': region_name}

    regionviews = layout.regionview_set.filter(region=region_name).order_by('weight')
    views = []

    for regionview in regionviews:
        view_vars={}
        view = cyc_site.get_view_options(
            regionview.content_type.model_class(),
            regionview.content_view,
            )
        if regionview.content_object:
            slug = regionview.content_object.slug
        else:
            slug=None

        view_vars['output'] = view(context['request'], inline=True, slug=slug)
        view_vars['name'] = regionview.content_view
        views.append(view_vars)

    region_vars['views'] = views

    return region_vars
