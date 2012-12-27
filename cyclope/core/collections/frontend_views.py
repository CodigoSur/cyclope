#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010 - 2012 Código Sur Sociedad Civil
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
from cyclope.frontend_views import MenuHierarchyOptions
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
        req_context.update({"categorizations": categorizations_list,
                            "category": category})
        t = loader.get_template(template)
        return t.render(req_context)

frontend.site.register_view(Category, CategoryRootItemsList)

class TeaserListOptions(forms.Form):
    show_title = forms.BooleanField(label=_("Show title"), initial=True, required=False)
    show_description = forms.BooleanField(label=_("Show description"), initial=True, required=False)
    show_image = forms.BooleanField(label=_("Show image"), initial=True, required=False)
    items_per_page = forms.IntegerField(label=_('Items per page'), min_value=1,
                                        initial=cyc_settings.CYCLOPE_PAGINATION['TEASER'],)
    limit_to_n_items = forms.IntegerField(label=_('Limit to N items (0 = no limit)'),
                                          min_value=0, initial=0)
    sort_by = forms.ChoiceField(label=_('Sort by'),
                              choices=(("DATE-", _(u"Date ↓ (newest first)")),
                                       ("DATE+", _(u"Date ↑ (oldest first)")),
                                       ("ALPHABETIC", _(u"Alphabetic")),
                                       ("RANDOM", _(u"Random"))),
                              initial="DATE-")
    simplified = forms.BooleanField(label=_("Simplified"), initial=False, required=False)
    traverse_children = forms.BooleanField(label=_("Include descendant's elements"),
                                                    initial=False, required=False)
    navigation = forms.ChoiceField(label=_('Show navigation'),
                              choices=(("TOP", _(u"Top")),
                                       ("BOTTOM", _(u"Bottom")),
                                       ("DISABLED", _(u"Disabled"))),
                              initial="TOP")


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
            view = frontend.site.get_view(content_object, view_name)
            if category.collection.view_options:
                options.update(category.collection.view_options)
            req_context['view_options'] = options
        else:
            view = frontend.site.get_view(content_object, 'teaser_list')
        return view.get_response(request, req_context, options, content_object)

frontend.site.register_view(Category, CategoryDefaultList)

SORT_BY = {
    "DATE-": ('creation_date', True, Paginator),
    "DATE+": ('creation_date', False, Paginator),
    "ALPHABETIC": ('name', None, NamePaginator),
    "RANDOM": ('random', False, Paginator),
}

def _get_paginator_page(category, options, request):
    traverse_children = options["traverse_children"]
    sort_by = options["sort_by"]
    limit = options["limit_to_n_items"] or None
    sort_property, reverse, paginator_class = SORT_BY[sort_by]
    search_args = [category, sort_property, limit, traverse_children]
    paginator, page = None, None
    if 'DATE' in sort_by:
        search_args.append(reverse)
    categorizations_list = Categorization.objects.get_for_category(*search_args)
    if options.get("items_per_page"):
        paginator_kwargs = {"per_page": options["items_per_page"]}
        if 'ALPHABETIC' in sort_by:
            paginator_kwargs['on'] = "content_object.name"
        paginator = paginator_class(categorizations_list, **paginator_kwargs)
        page = cyclope.utils.get_page(paginator, request)
    return categorizations_list, paginator, page

class CategoryTeaserList(frontend.FrontendView):
    """A teaser list view of Category members.
    """
    name = 'teaser_list'
    verbose_name = _('teaser list of Category members')
    is_content_view = True
    is_region_view = True
    options_form = TeaserListOptions
    inline_view_name = 'teaser'
    template = "collections/category_teaser_list.html"

    #TODO(nicoechaniz): find a more elegant way to build this view. current version is a temporary fix to a performance problem of the previous implementation when sorting big amounts of data.
    def get_response(self, request, req_context, options, content_object):
        category = content_object
        _, _, page = _get_paginator_page(category, options, request)
        req_context.update({'categorizations': page.object_list,
                            'page': page,
                            'category': category,
                            'inline_view_name': self.inline_view_name,
                            'simplified_view': options["simplified"]})
        t = loader.get_template(self.template)
        return t.render(req_context)

frontend.site.register_view(Category, CategoryTeaserList)


class CategoryLabeledIconList(CategoryTeaserList):
    """A labeled icon list view of Category members.
    """
    name='labeled_icon_list'
    verbose_name=_('labeled icon list of Category members')
    is_default = False
    items_per_page = cyc_settings.CYCLOPE_PAGINATION['LABELED_ICON']

    template = "collections/category_labeled_icon_list.html"
    inline_view_name = 'labeled_icon'

frontend.site.register_view(Category, CategoryLabeledIconList)


class SlideshowOptions(forms.Form):
    visualization_mode = forms.ChoiceField(label=_('Visual Mode'),
                              choices=(("slideshow", _(u"Standard view")),
                                       ("slideshow-background",
                                       _(u"With background image view"))),
                              initial="slideshow-background")
    show_title = forms.BooleanField(label=_("Show title"), initial=True, required=False)
    show_description = forms.BooleanField(label=_("Show description"), initial=True, required=False)
    show_image = forms.BooleanField(label=_("Show image"), initial=True, required=False)
    limit_to_n_items = forms.IntegerField(label=_('Limit to N items (0 = no limit)'),
                                          min_value=0, initial=10)
    sort_by = forms.ChoiceField(label=_('Sort by'),
                              choices=(("DATE-", _(u"Date ↓ (newest first)")),
                                       ("DATE+", _(u"Date ↑ (oldest first)")),
                                       ("ALPHABETIC", _(u"Alphabetic")),
                                       ("RANDOM", _(u"Random"))),
                              initial="DATE-")
    traverse_children = forms.BooleanField(label=_("Include descendant's elements"),
                                                    initial=False, required=False)
    scroll_by = forms.IntegerField(label=_('Scroll by N items'),
                               min_value=1, initial=3)
    speed = forms.IntegerField(label=_('Speed of transition (in milliseconds)'),
                               min_value=0, initial=1000)
    auto_play = forms.BooleanField(label=_("Automatic playback"),
                                   initial=True, required=False)
    auto_pause = forms.BooleanField(label=_("Stop automatic playback after click"),
                                    initial=True, required=False)
    delay = forms.IntegerField(label=_('Delay between transitions (seconds)'),
                               min_value=1, initial=3)
    circular = forms.BooleanField(label=_("Circular navigation"), initial=False,
                                  required=False)
    navigation = forms.ChoiceField(label=_('Navigation wrap'),
                              choices=(("'circular'", _(u"Circular")),
                                       ("'first'", _(u"First")),
                                       ("'last'", _(u"Last")),
                                       ("'both'", _(u"Both")),
                                       ("null", _(u"None"))),
                              initial="circular")

class CategorySlideshow(frontend.FrontendView):
    """A slideshow view of Category members.
    """
    name='slodeshow'
    verbose_name=_('slideshow of Category members')
    is_content_view = True
    is_region_view = True
    is_default = False
    options_form = SlideshowOptions
    inline_view_name = 'slideshow_item'
    template = "collections/category_slideshow.html"

    def get_response(self, request, req_context, options, content_object):
        category = content_object
        categorizations_list, _, _ = _get_paginator_page(category,
                                                         options,
                                                         request)
        req_context.update({'categorizations': categorizations_list,
                            'category': category,
                            'inline_view_name': self.inline_view_name,
                            'category_slug': category.slug
                            })
        t = loader.get_template(self.template)
        return t.render(req_context)

frontend.site.register_view(Category, CategorySlideshow)


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
    is_region_view = True
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
    options_form = MenuHierarchyOptions
    template = "collections/collection_categories_hierarchy.html"

    def get_response(self, request, req_context, options, content_object):
        collection = content_object
        categories = Category.tree.filter(collection=collection, level=0)
        category_list = []
        for category in categories:
            category_list.extend(self._get_categories_nested_list(category))
        req_context.update({'categories': category_list,
                            'collection_slug': collection.slug,
                            'align': options["align"]})
        t = loader.get_template(self.template)
        return t.render(req_context)

    def _get_categories_nested_list(self, base_category, name_field='name'):

        """Creates a nested list to be used with unordered_list template tag
        """
        #TODO(nicoechaniz): see if there's a more efficient way to build this recursive template data.
        from django.template import Template, Context
        link_template = Template(
              '<span class="{{ has_children }} {{ has_content}}">'
                '<a href="{% url category-'+ self.target_view +' slug %}">'
                 '{{ name }}</a>'
              '</span>'
            )

        def item_context(item):
            name = getattr(item, name_field)
            has_content = 'has_content' if item.categorizations.exists()\
                          else 'no_content'
            has_children = 'has_children' if item.get_descendant_count()\
                           else 'no_children'
            context = Context({'name': name,
                               'slug': item.slug,
                               'has_content': has_content,
                               'has_children': has_children,})
            return context

        nested_list = []
        for child in base_category.get_children():
            if child.get_descendant_count()>0:
                nested_list.extend(self._get_categories_nested_list(
                    child, name_field=name_field))
            else:
                nested_list.append(link_template.render(item_context(child)))

        include = link_template.render(item_context(base_category))
        if nested_list:
            return [include, nested_list]
        else:
            return [include]

frontend.site.register_view(Collection, CollectionCategoriesHierarchy)

class CollectionCategoriesHierarchyToIconlist(CollectionCategoriesHierarchy):
    """A hierarchical list view of the Categories in a Collection that will
    show a labeled_icon list view of the category that the user makes a
    selection.
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
        categorizations_list = Categorization.objects.get_for_category(
                                  category, 'modification_date', reverse=True)

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
                obj.last_comment_author = last_comment.user_name

        req_context.update({'categorizations': page.object_list,
                            'page': page,
                            'category': category})
        t = loader.get_template(self.template)
        return t.render(req_context)

frontend.site.register_view(Category, CategoryListAsForum)
