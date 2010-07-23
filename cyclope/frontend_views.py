# *-- coding:utf-8 --*
"""cyclope.frontend_views"""

from django.utils.translation import ugettext_lazy as _
from django.template import loader, RequestContext
from django.contrib.sites.models import Site

from cyclope import settings as cyc_settings
from cyclope.core import frontend
from cyclope.models import Menu, MenuItem
from cyclope import views

class SiteBreadcrumb(frontend.FrontendView):
    """Navigation breadcrumb
    """
    name='breadcrumb'
    verbose_name=_('navigation breadcrumb')
    is_default = True
    is_instance_view = False

    def get_string_response(self, request, content_object=None, *args, **kwargs):
        menu_items = MenuItem.tree.filter(menu=content_object, level=0)
        c = RequestContext(request, {'menu_items': menu_items})
        t = loader.get_template("cyclope/breadcrumb.html")
        c['host_template'] = 'cyclope/inline_view.html'
        return t.render(c)

frontend.site.register_view(Site, SiteBreadcrumb())


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

#############
