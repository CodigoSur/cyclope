# *-- coding:utf-8 --*

from django.utils.translation import ugettext as _

from cyclope.core import frontend
from cyclope import views

from models import Article


class ArticleDetailView(frontend.FrontendView):
    """Detail view for Articles"""
    name='detail'
    verbose_name=_('detailed view of the selected Article')
    is_default = True
    params = {'queryset': Article.objects,
              'template_object_name': 'article',
             }

    def get_http_response(self, request, slug=None, *args, **kwargs):
        return views.object_detail(request, slug=slug,
                                   inline=False, *args, **kwargs)

frontend.site.register_view(Article, ArticleDetailView())


class ArticleTeaserList(frontend.FrontendView):
    """Teaser list view for Articles.
    """
    name='teaser_list'
    verbose_name=_('list of Article teasers')
    is_instance_view = False
    params = { 'template_name': 'articles/article_teaser_list.html' }

    def get_http_response(self, request, *args, **kwargs):
        return views.object_list(request,
                           queryset=Article.objects.all(),
                           template_object_name= 'article',
                           *args, **kwargs)

    def get_string_response(self, request, *args, **kwargs):
        return views.object_list(request, inline=True,
                           queryset=Article.objects.all(),
                           template_object_name= 'article',
                           *args, **kwargs)

frontend.site.register_view(Article, ArticleTeaserList())
