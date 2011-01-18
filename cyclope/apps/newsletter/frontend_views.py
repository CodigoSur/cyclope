from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse
from django.template.loader import get_template

from cyclope.core import frontend
from cyclope.apps.newsletter.models import Newsletter
from cyclope.core.collections.models import Category

class NewsletterCurrentContentTeasers(frontend.FrontendView):
    """Teaser list of the current content for a Newsletter"""
    name='current_content_teasers'
    verbose_name=_('show the current content teasers for the selected Newsletter')
    is_default = True
    is_instance_view = True
    is_content_view = True
    is_region_view = False

    category_view = 'teaser_list'    

    def get_response(self, request, req_context, content_object):
        newsletter = content_object
        view = frontend.site.get_view(Category, self.category_view)
        result = view.get_response(request, req_context,
                                   content_object=newsletter.content_category)
        return result

frontend.site.register_view(Newsletter, NewsletterCurrentContentTeasers)


class NewsletterCurrentContent(NewsletterCurrentContentTeasers):
    """List of the current content for a Newsletter"""
    name='current_content'
    verbose_name=_('show the current content for the selected Newsletter')
    is_default = False
    is_instance_view = True
    is_content_view = True
    is_region_view = False

    category_view = 'contents'
    
frontend.site.register_view(Newsletter, NewsletterCurrentContent)


class NewsletterHeader(frontend.FrontendView):
    """Header of a Newsletter"""
    name='header'
    verbose_name=_('show the header text of the selected Newsletter')
    is_instance_view = True
    is_region_view = True
    
    def get_response(self, request, req_context, content_object):
        newsletter = content_object
        return newsletter.header

frontend.site.register_view(Newsletter, NewsletterHeader)
