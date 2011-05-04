#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

from django import forms
from django.template import loader
from django.core.urlresolvers import reverse
from django.contrib.comments.models import Comment
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator

import cyclope.utils
from cyclope.utils import NamePaginator
from cyclope.core import frontend
from cyclope import settings as cyc_settings
from cyclope.core.collections.models import Collection, Category, Categorization


class CategoryRootItemsList(frontend.FrontendView):
    """A flat list view of the root members for a Category.
    """
    name='root_items_list'
    verbose_name=_('list of root items for the selected Category')

    is_content_view = True
    is_region_view = True

    def get_response(self, request, req_context, options, content_object):
        category = content_object
        categorizations_list = category.categorizations.all()
        template = "collections/category_root_items_list.html"
        req_context['categorizations'] = categorizations_list
        t = loader.get_template(template)
        return t.render(req_context)

frontend.site.register_view(Category, CategoryRootItemsList)

class TeaserListOptions(forms.Form):
    items_per_page = forms.IntegerField(label=_('Items per page'), min_value=1,
                                        initial=cyc_settings.CYCLOPE_PAGINATION['TEASER'],)
    sort_by = forms.ChoiceField(label=_('Sort by'),
                              choices=(("DATE-", _(u"Date ↓ (newest first)")),
                                       ("DATE+", _(u"Date ↑ (oldest first)")),
                                       ("ALPHABETIC", _(u"Alphabetic"))),
                              initial="DATE-")
    simplified = forms.BooleanField(label=_("Simplified"), initial=False, required=False)
    traverse_children = forms.BooleanField(label=_("Include descendant's elements"),
                                                    initial=False, required=False)

class CategoryDefaultList(frontend.FrontendView):
    name = 'default'
    verbose_name = _('default view for the Collection')
    is_default = True
    is_content_view = True
    options_form = TeaserListOptions

    def get_response(self, request, req_context, options, content_object):
        category = content_object
        if category.collection.default_list_view not in ["", self.name]:
            view_name = category.collection.default_list_view
            view = frontend.site.get_view(content_object.__class__, view_name)
        else:
            view = frontend.site.get_view(content_object.__class__, 'teaser_list')
        return view.get_response(request, req_context, options, content_object)

frontend.site.register_view(Category, CategoryDefaultList)

class CategoryTeaserList(frontend.FrontendView):
    """A teaser list view of Category members.
    """
    name = 'teaser_list'
    verbose_name = _('teaser list of Category members')

    is_content_view = True
    is_region_view = True
    options_form = TeaserListOptions
    inline_view_name = 'teaser'

    def get_response(self, request, req_context, options, content_object):
        category = content_object
        if options["traverse_children"]:
            own = category.categorizations.select_related().all()
            children_categories = category.get_descendants()
            children = Categorization.objects.select_related().filter(category__in=children_categories)
            categorizations_list = list(set(own | children))
        else:
            categorizations_list = category.categorizations.select_related().all()

        sort_by = options["sort_by"]
        if "DATE" in sort_by:
            if sort_by == "DATE-":
                reverse = True
            elif sort_by == "DATE+":
                reverse = False
            categorizations_list = sorted(categorizations_list,
                                          key=lambda c: c.object_modification_date,
                                          reverse=reverse)
            paginator = Paginator(categorizations_list, options["items_per_page"])
            template = "collections/category_teaser_list.html"

        elif sort_by == "ALPHABETIC":
            paginator = NamePaginator(categorizations_list, on="content_object.name",
                                      per_page=self.items_per_page)
            template = "collections/category_alphabetical_teaser_list.html"

        page = cyclope.utils.get_page(paginator, request)

        req_context.update({'categorizations': page.object_list,
                            'page': page,
                            'category': category,
                            'inline_view_name': self.inline_view_name,
                            'simplified_view': options["simplified"]})
        t = loader.get_template(template)
        return t.render(req_context)

frontend.site.register_view(Category, CategoryTeaserList)


class CategoryLabeledIconList(CategoryTeaserList):
    """A labeled icon list view of Category members.
    """
    name='labeled_icon_list'
    verbose_name=_('Labeled icon list of Category members')
    is_default = False
    items_per_page = cyc_settings.CYCLOPE_PAGINATION['LABELED_ICON']

    template = "collections/category_labeled_icon_list.html"
    inline_view_name = 'teaser'

frontend.site.register_view(Category, CategoryLabeledIconList)


class CategoryContents(CategoryTeaserList):
    """Full content of Category members.
    """
    name = 'contents'
    verbose_name = _('full content of Category members')
    items_per_page = cyc_settings.CYCLOPE_PAGINATION['DETAIL']
    is_content_view = True
    is_region_view = False

    template = "collections/category_contents.html"
    inline_view_name = 'inline_detail'

frontend.site.register_view(Category, CategoryContents)


class CollectionRootCategoriesTeaserList(frontend.FrontendView):
    """ A teaser list of the root Categories of a Collection
    """
    name = 'root_categories_teaser_list'
    verbose_name=_('teaser list of the root Categories of a Collection')
    is_default = True
    is_content_view = True
    template = "collections/collection_root_categories_teaser_list.html"

    def get_response(self, request, req_context, options, content_object):
        collection = content_object
        req_context.update(
            {'categories': Category.tree.filter(collection=collection, level=0),
             'collection': collection })
        t = loader.get_template(self.template)
        return t.render(req_context)

frontend.site.register_view(Collection, CollectionRootCategoriesTeaserList)

class CollectionRootCategoriesList(CollectionRootCategoriesTeaserList):
    """ A list of the root Categories of a Collection
    """
    name = 'root_categories_list'
    verbose_name=_('list of the root Categories of a Collection')
    is_default = False
    is_region_view = True
    template = "collections/collection_root_categories_list.html"

frontend.site.register_view(Collection, CollectionRootCategoriesList)


class CollectionCategoriesHierarchy(frontend.FrontendView):
    """A hierarchical list view of the Categories in a Collection.
    """
    name='categories_hierarchy'
    verbose_name=_('hierarchical list of Categories in a Collection')
    target_view = 'default'
    is_content_view = True
    is_region_view = True

    def get_response(self, request, req_context, options, content_object):
        collection = content_object
        categories = Category.tree.filter(collection=collection, level=0)
        category_list = []
        for category in categories:
            category_list.extend(self._get_categories_nested_list(category))
        req_context.update({'categories': category_list,
                            'collection_slug': collection.slug})
        template = "collections/collection_categories_hierarchy.html"
        t = loader.get_template(template)
        return t.render(req_context)

    def _get_categories_nested_list(self, base_category, name_field='name'):

        """Creates a nested list to be used with unordered_list template tag
        """
        #TODO(nicoechaniz): see if there's a more efficient way to build this recursive template data.
        #TODO(nicoechaniz): only show categories which have children or content.
        from django.template import Template, Context
        link_template = Template(
            '{% if has_content or has_children %}'
              '<span class="has_children">'
                '<a href="{% url category-'+ self.target_view +' slug %}">'
                 '{{ name }}</a>'
              '</span>'
            '{% else %}<span class="no_children">{{ name }}</span>'
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
        if nested_list:
            return [include, nested_list]
        else:
            return [include]

frontend.site.register_view(Collection, CollectionCategoriesHierarchy)

class CollectionCategoriesHierarchyToIconlist(CollectionCategoriesHierarchy):
    """A hierarchical list view of the Categories in a Collection that will show a labeled_icon list view of the category that the user makes a selection.
    """
    name='categories_hierarchy_to_iconlist'
    verbose_name=_('hierarchical list of Categories that will show an icon list on click')
    target_view = 'labeled_icon_list'

frontend.site.register_view(Collection, CollectionCategoriesHierarchyToIconlist)

class CollectionCategoriesMembersAlphabeticTeaserList(frontend.FrontendView):
    """An alphabetic teaser list of all the members of the collection's categories.
    """
    name='collection_all_items_teaser_list'
    verbose_name=_("alphabetical teaser list of all the members of the Collection's Categories")
    is_content_view = True
    is_region_view = True
    items_per_page = cyc_settings.CYCLOPE_PAGINATION['TEASER']

    template = "collections/collection_all_items_alphabetical_teaser_list.html"

    def get_response(self, request, req_context, options, content_object):
        collection = content_object
        categorizations_list = Categorization.objects.filter(category__in=collection.categories.all())
        object_list = list(set([cat.content_object for cat in categorizations_list]))

        paginator = NamePaginator(object_list, on="name", per_page=self.items_per_page)
        page = cyclope.utils.get_page(paginator, request)

        req_context.update({'object_list': page.object_list,
                            'page': page,
                            'collection': collection
                            })
        t = loader.get_template(self.template)
        return t.render(req_context)

frontend.site.register_view(Collection, CollectionCategoriesMembersAlphabeticTeaserList)

class CategoryListAsForum(frontend.FrontendView):
    """ A list view of Category Members that will show a table with some extra
        information of the content (creation_date, count of comments, etc)
    """
    name='list_as_forum'
    verbose_name=_('list of Category members as forum view')
    is_default = False
    items_per_page = cyc_settings.CYCLOPE_PAGINATION['FORUM']
    is_content_view = True
    is_region_view = True

    template = "collections/category_list_as_forum.html"

    def get_response(self, request, req_context, options, content_object):
        category = content_object
        categorizations_list = category.categorizations.all()

        # TODO(diegoM): ¡¡¡ No escala !!!
        categorizations_list = sorted(categorizations_list,
                                      key=lambda c: c.object_modification_date,
                                      reverse=True)

        paginator = Paginator(categorizations_list, self.items_per_page)
        page = cyclope.utils.get_page(paginator, request)

        for categorization in page.object_list:
            obj = categorization.content_object
            ct = ContentType.objects.get_for_model(obj)
            qs = Comment.objects.filter(content_type=ct,object_pk=obj.pk)
            obj.comments_count = qs.count()
            obj.url = reverse(categorization.content_type.model, args=[obj.slug])
            if obj.comments_count:
                last_comment = qs.latest('submit_date')
                obj.last_comment_date = last_comment.submit_date
                obj.last_comment_author = obj.author

        req_context.update({'categorizations': page.object_list,
                            'page': page,
                            'category': category})
        t = loader.get_template(self.template)
        return t.render(req_context)

frontend.site.register_view(Category, CategoryListAsForum)
