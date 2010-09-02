#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright 2010 Código Sur - Nuestra América Asoc. Civil / Fundación Pacificar.
# All rights reserved.
#
# This file is part of Cyclope.
#
# Cyclope is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Cyclope is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from django.utils.translation import ugettext_lazy as _

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

        content_object = self.params['queryset'].get(slug=slug)
        context = {'content_relations':
                   content_object.related_contents.all()}
        return views.object_detail(request, slug=slug, extra_context = context,
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

class ArticleLabeledIconList(ArticleTeaserList):
    """Labeled icon list view for Articles.
    """
    name='labeled_icon_list'
    verbose_name=_('list of Article labeled icons')
    is_instance_view = False
    params = { 'template_name': 'articles/article_labeled_icon_list.html' }

    #def get_http_response(self, request, *args, **kwargs):
    #    return views.object_list(request,
    #                       queryset=Article.objects.all(),
    #                       template_object_name= 'article',
    #                       *args, **kwargs)
    #
    #def get_string_response(self, request, *args, **kwargs):
    #    return views.object_list(request, inline=True,
    #                       queryset=Article.objects.all(),
    #                       template_object_name= 'article',
    #                       *args, **kwargs)

frontend.site.register_view(Article, ArticleLabeledIconList())
