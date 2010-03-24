# *-- coding:utf-8 --*
"""Views for ``Cyclope`` models."""

from django.utils.translation import ugettext as _
from django.views.generic.list_detail import object_list
from django.template import loader, RequestContext

from cyclope import settings as cyc_settings
from cyclope.core import frontend
from cyclope.models import StaticPage, Menu
from cyclope import views

def custom_list(request, *args, **kwargs):
    host_template = template_for_request(request)
    response = HttpResponse("hola %s" % host_template)
    return response

class MainMenuView(frontend.FrontendView):
    """A list view of the menuitems for the main menu.
    """
    name='main_menu_flat_list'
    verbose_name=_('flat list of main menu root items')
    is_default = True
    params = {'queryset': Menu.objects,
              'template_object_name': 'menu',
              }

    def get_string_response(self, request, inline=False, *args, **kwargs):
        print "nos llaman"
        main_menu = self.params['queryset'].get(main_menu=True)
        c = RequestContext(request, {'menu':main_menu})
        t = loader.get_template("cyclope/menu_flat_list.html")
        c['host_template'] = 'cyclope/inline_view.html'
        return t.render(c)

frontend.site.register_view(Menu, MainMenuView())

class StaticPageDetailView(frontend.FrontendView):
    """Detail view of a StaticPage.

    Returns:
        a string if the view is called from within a region templatetag
        an HttpResponse otherwise
    """
    name='detail'
    verbose_name=_('full detail')
    is_default = True
    params = {'queryset': StaticPage.objects,
              'template_object_name': 'staticpage',
             }

    def get_http_response(self, request, *args, **kwargs):
        return views.object_detail(request, inline=False, *args, **kwargs)

    def get_string_response(self, request, *args, **kwargs):
        return views.object_detail(request, inline=True, *args, **kwargs)

frontend.site.register_view(StaticPage, StaticPageDetailView())


class StaticPageListView(frontend.FrontendView):
    """Simple list view for a StaticPage.
    """
    name='list'
    verbose_name=_('page list')
    #params = {'queryset': StaticPage.objects,
    #          'template_object_name': 'staticpage',
    #         }
    is_instance_view = False

    def get_http_response(self, request, *args, **kwargs):
        return object_list(request,
                           queryset=StaticPage.objects.all(),
                           template_object_name= 'staticpage',
                           *args, **kwargs)

    def get_string_response(self, request, *args, **kwargs):
        return object_list(request,
                           queryset=StaticPage.objects.all(),
                           template_object_name= 'staticpage',
                           *args, **kwargs)

frontend.site.register_view(StaticPage, StaticPageListView())

#############
