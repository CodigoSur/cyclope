# *-- coding:utf-8 --*
"""cyclope.frontend_views"""

from django.utils.translation import ugettext as _
from django.views.generic.list_detail import object_list
from django.template import loader, RequestContext

from cyclope import settings as cyc_settings
from cyclope.core import frontend
from cyclope.models import StaticPage, Menu, MenuItem
from cyclope import views

def custom_list(request, *args, **kwargs):
    host_template = template_for_request(request)
    response = HttpResponse("hola %s" % host_template)
    return response

class MenuRootItemsList(frontend.FrontendView):
    """A flat list view of the menuitems for a given menu.
    """
    name='root_items_list'
    verbose_name=_('list of root items for the selected Menu')
    is_default = True

    def get_string_response(self, request, content_object=None, *args, **kwargs):
        menu_items = MenuItem.tree.filter(menu=content_object, level=0)
        c = RequestContext(request, {'menu_items': menu_items})
        t = loader.get_template("cyclope/menu_flat_list.html")
        c['host_template'] = 'cyclope/inline_view.html'
        return t.render(c)

frontend.site.register_view(Menu, MenuRootItemsList())


class StaticPageDetail(frontend.FrontendView):
    """Detail view of a StaticPage.

    Returns:
        a string if the view is called from within a region templatetag
        an HttpResponse otherwise
    """
    name='detail'
    verbose_name=_('detailed view of the selected Static Page')
    is_default = True
    params = {'queryset': StaticPage.objects,
              'template_object_name': 'staticpage',
             }

    def get_http_response(self, request, *args, **kwargs):
        return views.object_detail(request, inline=False, *args, **kwargs)

    def get_string_response(self, request, *args, **kwargs):
        return views.object_detail(request, inline=True, *args, **kwargs)

frontend.site.register_view(StaticPage, StaticPageDetail())


class StaticPageList(frontend.FrontendView):
    """Simple list view for a StaticPage.
    """
    name='list'
    verbose_name=_('list of Static Pages')
    #params = {'queryset': StaticPage.objects,
    #          'template_object_name': 'staticpage',
    #         }
    is_instance_view = False

    def get_http_response(self, request, *args, **kwargs):
        # FrontendView.__call__ will determine if the view is inline or not
        # and set inline kwarg accordingly
        return object_list(request,
                           queryset=StaticPage.objects.all(),
                           template_object_name= 'staticpage',
                           *args, **kwargs)

    def get_string_response(self, request, *args, **kwargs):
        # FrontendView.__call__ will determine if the view is inline or not
        # and set inline kwarg accordingly
        return object_list(request,
                           queryset=StaticPage.objects.all(),
                           template_object_name= 'staticpage',
                           *args, **kwargs)

frontend.site.register_view(StaticPage, StaticPageList())

#############
