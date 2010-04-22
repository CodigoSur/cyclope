# *-- coding:utf-8 --*

from django.utils.translation import ugettext as _
from django.views.generic.list_detail import object_detail, object_list

from cyclope.core import frontend
from cyclope import views

from models import Shoe

class ShoeDetailView(frontend.FrontendView):
    """Detail view for Shoes"""
    name='detail'
    verbose_name=_('full detail')
    is_default = True
    params = {'queryset': Shoe.objects,
              'template_object_name': 'shoe',
             }

    def get_http_response(self, request, *args, **kwargs):
        return views.object_detail(request, inline=False, *args, **kwargs)

frontend.site.register_view(Shoe, ShoeDetailView())


class ShoeList(frontend.FrontendView):
    """Simple list view for Shoes.
    """
    name='list'
    verbose_name=_('list of Shoes')
    is_instance_view = False

    def get_http_response(self, request, *args, **kwargs):
        return views.object_list(request,
                           queryset=Shoe.objects.all(),
                           template_object_name= 'shoe',
                           *args, **kwargs)

    def get_string_response(self, request, *args, **kwargs):
        return views.object_list(request, inline=True,
                           queryset=Shoe.objects.all(),
                           template_object_name= 'shoe',
                           *args, **kwargs)

frontend.site.register_view(Shoe, ShoeList())
