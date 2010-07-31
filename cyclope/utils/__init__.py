# *-- coding:utf-8 --*
"""
utils
-----
"""
from django.contrib.contenttypes.models import ContentType
import cyclope

def layout_for_request(request):
    """
    Returns the layout corresponding to the MenuItem matching the request URL
    or the default site layout if no matching MenuItem is found.
    """
    from cyclope.models import MenuItem

    req_url= request.META['PATH_INFO']
    req_url = req_url[len(cyclope.settings.CYCLOPE_PREFIX)+1:]

    if req_url == '':
        menu_item = MenuItem.objects.select_related().get(site_home=True)
    else:
        try:
            menu_item = MenuItem.objects.select_related().get(url=req_url)
        except:
            menu_item = None
    if menu_item and menu_item.layout:
        layout = menu_item.layout
    else:
        layout = cyclope.settings.CYCLOPE_DEFAULT_LAYOUT

    return layout


def template_for_request(request):
    """
    Returns the template corresponding to the MenuItem.layout
    matching the request or the default site template
    if no matching MenuItem is found.
    """
    layout = layout_for_request(request)
    template = 'cyclope/themes/%s/%s' % (
                cyclope.settings.CYCLOPE_CURRENT_THEME,
                layout.template
                )
    return template


from django.utils.functional import Promise
from django.utils.translation import force_unicode
from django.utils.simplejson import JSONEncoder

# snippet from http://code.djangoproject.com/ticket/5868
# to fix json encoding of lazy translated strings
class LazyJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, Promise):
            return force_unicode(o)
        else:
            return super(LazyJSONEncoder, self).default(o)
