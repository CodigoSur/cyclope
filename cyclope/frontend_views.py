# *-- coding:utf-8 --*
"""Views for ``Cyclope`` models."""

from django.utils.translation import ugettext as _
from django.views.generic.list_detail import object_list

from cyclope import settings as cyc_settings
from cyclope.core import frontend
from cyclope.models import StaticPage
from cyclope import views

def custom_list(request, *args, **kwargs):
    host_template = template_for_request(request)
    response = HttpResponse("hola %s" % host_template)
    return response

class StaticPageDetailView(frontend.FrontendView):
    """Detail view of a StaticPage

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

    def get_response(self, request, *args, **kwargs):
        return views.object_detail(request, *args, **kwargs)

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

    def get_response(self, request, *args, **kwargs):
        return object_list(request,
                           queryset=StaticPage.objects.all(),
                           template_object_name= 'staticpage',
                           *args, **kwargs)

frontend.site.register_view(StaticPage, StaticPageListView())

#############
