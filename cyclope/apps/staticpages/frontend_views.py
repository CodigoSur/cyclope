# *-- coding:utf-8 --*

from django.utils.translation import ugettext_lazy as _

from cyclope.core import frontend
from cyclope import views

from models import StaticPage

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

    def get_http_response(self, request, slug=None, *args, **kwargs):
        return views.object_detail(request, slug=slug,
                                   inline=False, *args, **kwargs)

    def get_string_response(self, request, content_object=None, *args, **kwargs):
        return views.object_detail(request, content_object=content_object,
                                   inline=True, *args, **kwargs)

frontend.site.register_view(StaticPage, StaticPageDetail())


class StaticPageList(frontend.FrontendView):
    """Simple list view for StaticPages.
    """
    name='list'
    verbose_name=_('list of Static Pages')
    #params = {'queryset': StaticPage.objects,
    #          'template_object_name': 'staticpage',
    #         }
    is_instance_view = False

    def get_http_response(self, request, *args, **kwargs):
        return views.object_list(request,
                           queryset=StaticPage.objects.all(),
                           template_object_name= 'staticpage',
                           *args, **kwargs)

    def get_string_response(self, request, *args, **kwargs):
        return views.object_list(request, inline=True,
                           queryset=StaticPage.objects.all(),
                           template_object_name= 'staticpage',
                           *args, **kwargs)

frontend.site.register_view(StaticPage, StaticPageList())
