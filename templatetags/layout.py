from copy import copy
from django import template
from cyclope import settings as cyc_settings, site as cyc_site
from cyclope.models import MenuItem, RegionView

register = template.Library()

@register.inclusion_tag('cyclope/region.html', takes_context=True)
def region(context, region_name):

    req_url= context['request'].META['PATH_INFO']

    if region_name == 'content':
        #print req_url
        #try:
        #    view_config = cyc_site._patterns[req_url]
        #    print view_config
        #except:
        #    pass
        return {}

#    content_url = req_url[len(cyc_settings.CYCLOPE_PREFIX):]
    try:
        menu_item = MenuItem.objects.select_related().get(url=req_url)
    except:
        menu_item = None
    if menu_item:
        layout = menu_item.layout
    else:
        layout = cyc_settings.CYCLOPE_DEFAULT_LAYOUT

    region_vars = {'layout_name': layout.slug, 'region_name': region_name}

    regionviews = layout.regionview_set.filter(region=region_name).order_by('weight')
    views = []
    for regionview in regionviews:
        view_vars={}
        view_config = cyc_site.get_view_config(
            regionview.content_type.model_class(),
            regionview.content_view,
            )
#        view_params = copy(view_config['view_params'])
#        view_params['extra_context'] = {'current_view_template': 'cyclope/inline_view.html'}

        view_vars['output'] = view_config['view'](context['request'],
                                          **view_config['view_params'])
        view_vars['name'] = regionview.content_view
        views.append(view_vars)

    region_vars['views'] = views

    return region_vars
