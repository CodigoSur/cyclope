# *-- coding:utf-8 --*

from django.utils.translation import ugettext as _
from django.views.generic.list_detail import object_detail, object_list

from cyclope.core import frontend
from cyclope import views

from cyclope.apps.articles.models import Article


class ArticleDetailView(frontend.FrontendView):
    """Detail view for Articles"""
    name='detail'
    verbose_name=_('detailed view of the selected Artiecle')
    is_default = True
    params = {'queryset': Article.objects,
              'template_object_name': 'article',
             }

    def get_http_response(self, request, slug=None, *args, **kwargs):
        return views.object_detail(request, slug=slug,
                                   inline=False, *args, **kwargs)

frontend.site.register_view(Article, ArticleDetailView())
