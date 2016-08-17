#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010 - 2015 Código Sur Sociedad Civil
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
from django.template.loader import render_to_string
from django.template import Context

import cyclope.utils
from cyclope.frontend_views import MenuHierarchyOptions
from cyclope.utils import NamePaginator, HyerarchyBuilderMixin
from cyclope.core import frontend
from cyclope import settings as cyc_settings
from cyclope.core.collections.models import Collection, Category, Categorization
from cyclope.core.collections.forms import ContentFilterForm

SORT_BY_FIELD_DEF = forms.ChoiceField(label=_('Sort by'),
                                      choices=(("DATE+", _(u"Date ↓ (newest first)")),
                                               ("DATE-", _(u"Date ↑ (oldest first)")),
                                               ("ALPHABETIC", _(u"Alphabetic")),
                                               ("RANDOM", _(u"Random"))),
                                      initial="DATE-")


class CategoryRootListOptions(forms.Form):
    show_title = forms.BooleanField(label=_("Show title"), initial=True, required=False)
    show_description = forms.BooleanField(label=_("Show description"), initial=True, required=False)
    show_image = forms.BooleanField(label=_("Show image"), initial=True, required=False)
    traverse_children = forms.BooleanField(label=_("Include descendant's elements"), initial=False, required=False)
    navigation = forms.ChoiceField(label=_('Show navigation'),
                                   choices=(("TOP", _(u"Top")),
                                            ("BOTTOM", _(u"Bottom")),
                                            ("DISABLED", _(u"Disabled"))),
                                   initial="TOP")


class CategoryRootItemsList(frontend.FrontendView):
    """A flat list view of the root members for a Category.
    """
    name = 'root_items_list'
    verbose_name = _('list of root items for the selected Category')

    is_content_view = True
    is_region_view = True
    options_form = CategoryRootListOptions
    
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
    sort_by = SORT_BY_FIELD_DEF
    simplified = forms.BooleanField(label=_("Simplified"), initial=False, required=False)
    traverse_children = forms.BooleanField(label=_("Include descendant's elements"),
                                           initial=False, required=False)
    navigation = forms.ChoiceField(label=_('Show navigation'),
                                   choices=(("TOP", _(u"Top")),
                                            ("BOTTOM", _(u"Bottom")),
                                            ("DISABLED", _(u"Disabled"))),
                                   initial="TOP")


class FilteredListOptions(forms.Form):
    items_per_page = forms.IntegerField(label=_('Items per page'), min_value=1,
                                        initial=cyc_settings.CYCLOPE_PAGINATION['TEASER'],)
    limit_to_n_items = forms.IntegerField(label=_('Limit to N items (0 = no limit)'),
                                          min_value=0, initial=0)
    sort_by = SORT_BY_FIELD_DEF

# traverse_children is not yet implemented for multiple categories
# TODO(nicoechaniz): evaluate if it could be implemented in a reasonably efficient way
#    traverse_children = forms.BooleanField(label=_("Include descendant's elements"),
#                                                    initial=False, required=False)
    intersection = forms.BooleanField(label=_("Only show content matching all filters"),
                                     initial=False, required=False)
    collection_filters = forms.MultipleChoiceField(label=_('Collections to use for category filters'),
                                                   choices=Collection.objects.all().values_list("slug", "name"),
                                                   required=False)


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
    "ALPHABETIC": ('name', False, NamePaginator), # TODO(nicoechaniz): reverse was None here, test and remove this comment
    "RANDOM": ('random', False, Paginator),
}


def _get_paginator_page(category, options, request):
    traverse_children = options.get("traverse_children", False)
    intersection = options.get("intersection", False)
    sort_by = options["sort_by"]
    limit = options["limit_to_n_items"] or None
    sort_property, reverse, paginator_class = SORT_BY[sort_by]
    try:
        iter(category)
        search_args = [category, sort_property, limit, traverse_children, reverse, intersection]
    except:
        search_args = [[category], sort_property, limit, traverse_children, reverse, intersection]
        
    paginator, page = None, None

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


class CategoryFilteredList(frontend.FrontendView):
    """A filtered list view of Category members.
       Supports filtering on multiple collections at once.
    """
    name = 'filtered_list'
    verbose_name = _('filtered list of Category members')
    is_instance_view = False
    is_content_view = True
    is_region_view = True
    options_form = FilteredListOptions
    inline_view_name = 'teaser'
    template = "collections/category_filtered_list.html"

    def get_response(self, request, req_context, options):
        col_filters = options["collection_filters"]
        if col_filters:
            collections =  Collection.objects.filter(slug__in=col_filters)
        else:
            collections = Collection.objects.none()

        form = ContentFilterForm(collections, request.GET)

        category_ids = []
        for collection in collections:
            category_id = request.GET.get(collection.slug)
            if category_id != "":
                try: category_id = int(category_id)
                except: continue
                category_ids.append(category_id)

        categories = Category.objects.filter(pk__in=category_ids)
        _, _, page = _get_paginator_page(categories, options, request)

        req_context.update({'categorizations': page.object_list,
                            'page': page,
                            'inline_view_name': self.inline_view_name,
                            'form': form
                            })
        t = loader.get_template(self.template)
        return t.render(req_context)

frontend.site.register_view(Category, CategoryFilteredList)


class CategoryLabeledIconList(CategoryTeaserList):
    """A labeled icon list view of Category members.
    """
    name = 'labeled_icon_list'
    verbose_name = _('labeled icon list of Category members')
    is_default = False
    items_per_page = cyc_settings.CYCLOPE_PAGINATION['LABELED_ICON']

    template = "collections/category_labeled_icon_list.html"
    inline_view_name = 'labeled_icon'

frontend.site.register_view(Category, CategoryLabeledIconList)


class CarrouselOptions(forms.Form):
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
    sort_by = SORT_BY_FIELD_DEF
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

class CategoryCarrousel(frontend.FrontendView):
    """A carrousel view of Category members for Bootstrap based themes.
    """
    name = 'carrousel'
    verbose_name = _('carousel view of Category members.')
    inline_view_name = 'carousel_item'
    template = "collections/category_carousel.html"
    is_content_view = True
    is_region_view = True
    is_default = False
    options_form = CarrouselOptions

    def get_response(self, request, req_context, options, content_object):
        category = content_object
        categorizations_list, _, _ = _get_paginator_page(category, options, request)
        req_context.update({'categorizations': categorizations_list,
                            'category': category,
                            'inline_view_name': self.inline_view_name,
                            'category_slug': category.slug
                            })
        t = loader.get_template(self.template)
        return t.render(req_context)

frontend.site.register_view(Category, CategoryCarrousel)


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
    verbose_name = _('list of the root Categories of a Collection')
    is_default = False
    is_region_view = True
    template = "collections/collection_root_categories_list.html"

frontend.site.register_view(Collection, CollectionRootCategoriesList)


class CollectionCategoriesHierarchy(frontend.FrontendView, HyerarchyBuilderMixin):
    """A hierarchical list view of the Categories in a Collection.
    """
    name='categories_hierarchy'
    verbose_name=_('hierarchical list of Categories in a Collection')
    target_view = 'default'
    is_content_view = True
    is_region_view = True
    options_form = MenuHierarchyOptions
    template = "collections/collection_categories_hierarchy.html"
    if cyc_settings.CYCLOPE_THEME_TYPE == 'bootstrap':
        template_item = "collections/collection_categories_hierarchy_item_bootstrap.html"
    else:
        template_item = "collections/collection_categories_hierarchy_item.html"

    def get_response(self, request, req_context, options, content_object):
        collection = content_object
        categories = Category.tree.filter(collection=collection, level=0)
        category_list = []
        for category in categories:
            category_list.extend(self.make_nested_list(category, True))
        req_context.update({'categories': category_list,
                            'collection_slug': collection.slug,
                            'align': options["align"]})
        t = loader.get_template(self.template)
        return t.render(req_context)

    def render_item(self, item, *args):
        has_children = 'has_children' if item.get_descendant_count()\
                       else 'no_children'
        context = Context({'name': item.name,
                           'slug': item.slug,
                           'has_children': has_children,
                           'target_view': "category-" + self.target_view})
        return render_to_string(self.template_item, context)

frontend.site.register_view(Collection, CollectionCategoriesHierarchy)


class CollectionCategoriesHierarchyToIconlist(CollectionCategoriesHierarchy):
    """A hierarchical list view of the Categories in a Collection that will
    show a labeled_icon list view of the category that the user makes a
    selection.
    """
    name = 'categories_hierarchy_to_iconlist'
    verbose_name = _('hierarchical list of Categories that will show an icon list on click')
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


class CategoryListAsForumOptions(forms.Form):
    show_title = forms.BooleanField(label=_("Show title"), initial=True, required=False)
    show_description = forms.BooleanField(label=_("Show description"), initial=True, required=False)
    show_image = forms.BooleanField(label=_("Show image"), initial=True, required=False)
    items_per_page = forms.IntegerField(label=_('Items per page'), min_value=1,
                                        initial=cyc_settings.CYCLOPE_PAGINATION['TEASER'],)
    limit_to_n_items = forms.IntegerField(label=_('Limit to N items (0 = no limit)'),
                                          min_value=0, initial=0)
    sort_by = SORT_BY_FIELD_DEF
    simplified = forms.BooleanField(label=_("Simplified"), initial=False, required=False)
    navigation = forms.ChoiceField(label=_('Show navigation'),
                                   choices=(("TOP", _(u"Top")),
                                   ("BOTTOM", _(u"Bottom")),
                                   ("DISABLED", _(u"Disabled"))),
                                   initial="TOP")


class CategoryListAsForum(frontend.FrontendView):
    """ A list view of Category Members that will show a table with some extra
        information of the content (creation_date, count of comments, etc)
    """
    name='list_as_forum'
    verbose_name=_('list of Category members as forum view')
    is_default = False
    items_per_page = cyc_settings.CYCLOPE_PAGINATION['FORUM']
    is_content_view = True
    is_region_view = False
    options_form = CategoryListAsForumOptions

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
