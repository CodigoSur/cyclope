from django.utils.translation import ugettext as _
from django.views.generic.list_detail import object_list

import cyclope.settings as cyc_settings
from cyclope import site as cyc_site
from cyclope.core import frontend

from cyclope.models import StaticPage
from cyclope import views

def custom_list(request, *args, **kwargs):
    host_template = template_for_request(request)
    response = HttpResponse("hola %s" % host_template)
    return response

class StaticPageDetailView(frontend.FrontendView):
    name='detail'
    verbose_name=_('full detail')
    is_default = True
    params = {'queryset': StaticPage.objects,
              'template_object_name': 'staticpage',
             }

    def get_response(self, request, *args, **kwargs):
        return views.object_detail(request, *args, **kwargs)

cyc_site.register_view(StaticPage, StaticPageDetailView())


class StaticPageListView(frontend.FrontendView):
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

cyc_site.register_view(StaticPage, StaticPageListView())

#############
