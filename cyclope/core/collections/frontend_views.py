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

"""cyclope.frontend_views"""

from django.utils.translation import ugettext_lazy as _
from django.template import loader, RequestContext
from django.http import Http404, HttpResponse
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from cyclope import settings as cyc_settings
from cyclope.core import frontend
from cyclope.core.collections.models import Collection, Category
from cyclope.utils import template_for_request

class CategoryRootItemsList(frontend.FrontendView):
    """A flat list view of category members.
    """
    name='root_items_list'
    verbose_name=_('list of root items for the selected Category')

    def get_string_response(self, request, content_object=None, *args, **kwargs):
        category = content_object
        c = RequestContext(request,
                           {'categorizations': category.categorizations.all()})
        t = loader.get_template("collections/category_root_items_list.html")
        c['host_template'] = 'cyclope/inline_view.html'
        return t.render(c)

    def get_http_response(self, request, slug=None, *args, **kwargs):
        category = Category.objects.get(slug=slug)
        c = RequestContext(request,
                           {'categorizations': category.categorizations.all()})
        t = loader.get_template("collections/category_root_items_list.html")
        c['host_template'] = template_for_request(request)
        return HttpResponse(t.render(c))

frontend.site.register_view(Category, CategoryRootItemsList())


class CategoryTeaserList(frontend.FrontendView):
    """A teaser list view of category members.
    """
    name='teaser_list'
    verbose_name=_('teaser list of Category members')
    is_default = True
    template = "collections/category_teaser_list.html"
    def get_string_response(self, request, content_object=None, *args, **kwargs):
        category = content_object
        #TODO(nicoechaniz): this article__date ordering looks bad. categories can hold any baseontent derivative
        c = RequestContext(request,
                           {'categorizations': category.categorizations.order_by('article__date'),
                            'category': category})
        t = loader.get_template(self.template)
        c['host_template'] = 'cyclope/inline_view.html'
        return t.render(c)

    def get_http_response(self, request, slug=None, *args, **kwargs):
        category = Category.objects.get(slug=slug)
        # TODO(nicoechaniz):this hardcoded order_by es wrong. fix it.
        categorizations_list = category.categorizations.order_by('article__date')

        paginator = Paginator(categorizations_list, cyc_settings.CYCLOPE_PAGINATION['TEASER'])

        # Make sure page request is an int. If not, deliver first page.
        try:
            page_number = int(request.GET.get('page', '1'))
        except ValueError:
            page_number = 1

        # DjangoDocs uses page differently
        # If page request (9999) is out of range, deliver last page of results.
        try:
            page = paginator.page(page_number)
        except (EmptyPage, InvalidPage):
            page = paginator.page(paginator.num_pages)

        c = RequestContext(request,
                           {'categorizations': page.object_list,
                            'page': page,
                            'category': category })
        t = loader.get_template(self.template)
        c['host_template'] = template_for_request(request)
        return HttpResponse(t.render(c))

frontend.site.register_view(Category, CategoryTeaserList())

class CategoryLabeledIconList(CategoryTeaserList):
    """A labeled icon list view of category members.
    """
    name='labeled_icon_list'
    verbose_name=_('Labeled icon list of Category members')
    template = "collections/category_labeled_icon_list.html"
    is_default = False

frontend.site.register_view(Category, CategoryLabeledIconList())

class CategorySimplifiedTeaserList(frontend.FrontendView):
    """A teaser list view of category members.
    """
    name='simplified_teaser_list'
    verbose_name=_('simplified teaser list of Category members')

    def get_string_response(self, request, content_object=None, *args, **kwargs):
        category = content_object
        c = RequestContext(request,
                           {'categorizations': category.categorizations.all(),
                            'category': category,
                            'simplified_view': True})
        t = loader.get_template("collections/category_teaser_list.html")
        c['host_template'] = 'cyclope/inline_view.html'
        return t.render(c)

frontend.site.register_view(Category, CategorySimplifiedTeaserList())


class CollectionRootCategoriesTeaserList(frontend.FrontendView):
    """ A teaser list of the root categories of a collection
    """
    name = 'root_categories_teaser_list'
    verbose_name=_('teaser list of the root Categories of a Collection')
    is_default = True

    def get_http_response(self, request, slug=None, *args, **kwargs):
        collection = Collection.objects.get(slug=slug)
        c = RequestContext(
            request,
            {'categories': Category.tree.filter(collection=collection, level=0),
             'collection': collection })
        t = loader.get_template("collections/collection_root_categories_teaser_list.html")
        c['host_template'] = template_for_request(request)
        return HttpResponse(t.render(c))

frontend.site.register_view(Collection, CollectionRootCategoriesTeaserList())


class CollectionCategoriesHierarchy(frontend.FrontendView):
    """A full list view of the categories in a collection.
    """
    name='categories_hierarchy'
    verbose_name=_('hierarchical list of Categories in a Collection')

    def get_string_response(self, request, content_object=None, *args, **kwargs):
        collection = content_object
        categories = Category.tree.filter(collection=collection, level=0)
        category_list = []
        for category in categories:
            category_list.extend(self._get_categories_nested_list(category))
        c = RequestContext(request, {'categories': category_list})
        t = loader.get_template("collections/collection_categories_hierarchy.html")
        c['host_template'] = 'cyclope/inline_view.html'
        return t.render(c)

    def _get_categories_nested_list(self, base_category, name_field='name'):
        """Creates a nested list to be uses with unordered_list template tag
        """
        #TODO(nicoechaniz): see if there's a more efficient way to build this recursive template data.
        #TODO(nicoechaniz): only show categories which have children or content.
        from django.template import Template, Context
        link_template = Template(
            '{% if has_children %}'
              '<span class="expand_collapse">+</span>\n'
            '{% endif %}'
            '{% if has_content %}'
              '<a href="{% url category-teaser_list slug %}" '
                 'class="{{class}}"><span>{{ name }}</span></a>'
            '{% else %} {{ name }}'
            '{% endif %}'
            )
        nested_list = []
        for child in base_category.get_children():
            if child.get_descendant_count()>0:
                nested_list.extend(self._get_categories_nested_list(
                    child, name_field=name_field))
            else:
                name = getattr(child, name_field)
                has_content = child.categorizations.exists()
                nested_list.append(link_template.render(
                    Context({'name': name,
                             'slug': child.slug,
                             'has_content': has_content,})))

        name = getattr(base_category, name_field)
        has_content = base_category.categorizations.exists()
        include = link_template.render(
            Context({'name': name,
                     'slug': base_category.slug,
                     'has_content': has_content,
                     'has_children': base_category.get_descendant_count()}))
        return [include, nested_list]

frontend.site.register_view(Collection, CollectionCategoriesHierarchy())
