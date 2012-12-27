from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse
from django.template import loader

from cyclope.core import frontend
from cyclope.apps.newsletter.models import Newsletter
from cyclope.core.collections.models import Category, Categorization

class NewsletterContentTeasers(frontend.FrontendView):
    """Teaser list for a Newsletter rendered as a table"""
    name='content_teasers_as_table'
    verbose_name=_('show content teasers linked to the website')
    is_default = True
    is_instance_view = True
    is_content_view = True
    is_region_view = False

    template = "newsletter/content_teasers.html"

    def get_response(self, request, req_context, options, content_object):
        newsletter = content_object
        category = newsletter.content_category
        categorizations_list = Categorization.objects.get_for_category(category, 'creation_date')

        req_context.update({'category': category,
                            'newsletter': newsletter,
                            'categorizations': categorizations_list,
                            'inline_view_name': 'newsletter_teaser',
                            })
        t = loader.get_template(self.template)
        return t.render(req_context)

frontend.site.register_view(Newsletter, NewsletterContentTeasers)


class NewsletterContent(NewsletterContentTeasers):
    """Teaser list for a Newsletter rendered as a table"""
    name='content'
    verbose_name=_('show the full content (no external links)')
    is_default = False
    is_instance_view = True
    is_content_view = True
    is_region_view = False

    template = "newsletter/content.html"

frontend.site.register_view(Newsletter, NewsletterContent)

## class NewsletterHeader(frontend.FrontendView):
##     """Header of a Newsletter"""
##     name='header'
##     verbose_name=_('Header')
##     is_instance_view = True
##     is_region_view = True

##     def get_response(self, request, req_context, options, content_object):
##         newsletter = content_object
##         return newsletter.header

## frontend.site.register_view(Newsletter, NewsletterHeader)
