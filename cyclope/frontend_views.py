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

"""
cyclope.frontend_views
----------------------
"""
from operator import attrgetter

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.template import Template, Context
from django.contrib.sites.models import Site
from django.contrib.comments.models import Comment
from django.template.loader import render_to_string

import cyclope.utils
from cyclope import settings as cyc_settings
from cyclope.core import frontend
from cyclope.core.collections.models import Collection, Category
from cyclope.models import Menu, MenuItem, Author


class MenuRootItemsList(frontend.FrontendView):
    """A list view of the root MenuItems for a given Menu.
    """
    name='root_items_list'
    verbose_name=_('list of root items for the selected Menu')
    is_default = True
    is_region_view = True
    template = "cyclope/menu_flat_items_list.html"

    def get_response(self, request, req_context, options, content_object):
        menu_items = MenuItem.tree.filter(menu=content_object,
                                          level=0, active=True)
        current_url = request.path_info[1:].split('/')[0]
        return render_to_string(self.template, {
            'menu_items': menu_items,
            'current_url': current_url
        }, req_context)


frontend.site.register_view(Menu, MenuRootItemsList)


class MenuFlatItemsList(frontend.FrontendView):
    """A flat list view of all the MenuItems for a given Menu.
    """
    name='flat_items_list'
    verbose_name=_('flat list of all items for the selected Menu')
    is_region_view = True
    template = "cyclope/menu_flat_items_list.html"

    def get_response(self, request, req_context, options, content_object):
        menu_items = MenuItem.tree.filter(menu=content_object, active=True)
        current_url = request.path_info[1:].split('/')[0]
        return render_to_string(self.template, {
            'menu_items': menu_items,
            'current_url': current_url
        }, req_context)


frontend.site.register_view(Menu, MenuFlatItemsList)

class MenuHierarchyOptions(forms.Form):
    align = forms.ChoiceField(label=_('Collapse style'),
                              choices=(("VERTICAL", _("vertical")),
                                       ("HORIZONTAL", _("horizontal")),
                                       ("ON_CLICK", _("on click")),
                                       ("DISABLED", _("disabled"))),
                              initial="HORIZONTAL")

# TODO(nicoechaniz): refactor this view and CollectionCategoriesHierarchy which share most of their code.
class MenuMenuItemsHierarchy(frontend.FrontendView):
    """A hierarchical list view of the menu items in a menu.
    """
    name='menuitems_hierarchy'
    verbose_name=_('hierarchical list of the items in the selected menu')
    is_region_view = True
    options_form = MenuHierarchyOptions
    template = "cyclope/menu_menuitems_hierarchy.html"

    def get_response(self, request, req_context, options, content_object):
        menu = content_object
        menu_items = MenuItem.tree.filter(menu=menu, level=0, active=True)
        menu_items_list = []
        current_url = request.path_info[1:]
        for item in menu_items:
            menu_items_list.extend(self._get_menuitems_nested_list(item, current_url))
        return render_to_string(self.template, {
            'menu_items': menu_items_list,
            'menu_slug': menu.slug,
            'expand_style': options["align"]
        }, req_context)

    def _get_menuitems_nested_list(self, base_item, current_url=None, name_field='name'):
        """Creates a nested list to be used with unordered_list template tag
        """
        #TODO(nicoechaniz): see if there's a more efficient way to build this recursive template data.
        link_template = Template(
             '<span class="{% if has_children %}has_children{% else %}no_children{% endif %}{% if current_url == menu_item.url%} current{% endif%}{% if menu_item.site_home %} site_home{% endif %}">'
             '{% if menu_item.custom_url %}'
             '   <a href="{{menu_item.url}}">'
             '{% else %}'
             '   <a href="/{{CYCLOPE_PREFIX}}{{menu_item.url}}">'
             '{% endif %}'
             '{{ menu_item.name }}</a></span>'
            )
        nested_list = []
        for child in base_item.get_children().filter(active=True):
            if child.get_descendant_count() > 0:
                nested_list.extend(self._get_menuitems_nested_list(
                    child, current_url, name_field=name_field))
            else:
                name = getattr(child, name_field)
                nested_list.append(link_template.render(
                    Context({'menu_item': child, 'current_url': current_url})))

        name = getattr(base_item, name_field)
        include = link_template.render(
            Context({'menu_item': base_item, 'current_url': current_url,
                     'has_children': base_item.get_descendant_count()}))
        if nested_list:
            return [include, nested_list]
        else:
            return [include]

frontend.site.register_view(Menu, MenuMenuItemsHierarchy)


class MenuItemChildrenOfCurrentItem(frontend.FrontendView):
    """List view of all the sub-items for the currently selected MenuItem
    """
    name='children_list'
    verbose_name=_('list view of children of the current menu item')
    is_default = True
    is_instance_view = False
    is_region_view = True
    template = "cyclope/menu_flat_items_list.html"
    def get_response(self, request, req_context, options):
        base_url = request.path_info[1:].split('/')[0]
        if base_url == '':
            current_item = MenuItem.tree.filter(site_home=True)
        else:
            current_item = MenuItem.tree.filter(url=base_url)

        if current_item:
            children = current_item[0].get_children().filter(active=True)
            return render_to_string(self.template, {'menu_items': children},
                                    req_context)
        else:
            return ''

frontend.site.register_view(MenuItem, MenuItemChildrenOfCurrentItem)


class SiteSearchBox(frontend.FrontendView):
    """Show a small form with an input field to search content
    """
    name='search'
    verbose_name=_('search box')
    is_instance_view = False
    is_region_view = True
    template = "cyclope/site_search_box.html"

    def get_response(self, request, req_context, options):
        return render_to_string(self.template, {}, req_context)

frontend.site.register_view(Site, SiteSearchBox)


class SiteMap(frontend.FrontendView):
    """Show an expanded hierarchical list of all collection and menus
    """
    name='map'
    verbose_name=_('sitemap view of the site')
    is_default = True
    is_instance_view = False
    is_content_view = True
    template = "cyclope/site_map.html"

    def get_response(self, request, req_context, options):
        collections_list = []
        for collection in Collection.objects.filter(visible=True):
            category_list = []
            for category in Category.tree.filter(collection=collection, level=0):
                # TODO(diegoM): Change this line when the refactorization is done
                category_list.extend(self._get_categories_nested_list(category))
            if category_list:
                collections_list.extend([collection,category_list])
            else:
                collections_list.append(collection)

        menus_list = []
        for menu in Menu.objects.all():
            menu_items_list = []
            for item in MenuItem.tree.filter(menu=menu, level=0):
                # TODO(diegoM): Change this line when the refactorization is done
                menu_items_list.extend(
                    MenuMenuItemsHierarchy()._get_menuitems_nested_list(item))
            if menu_items_list:
                menus_list.extend([menu.name, menu_items_list])
            else:
                menus_list.append(menu.name)

        return render_to_string(self.template, {
            'collections':collections_list,
            'menus':menus_list,
        }, req_context)

    def _get_categories_nested_list(self, base_category, name_field='name'):

        """Creates a nested list to be used with unordered_list template tag
        """
        #TODO(nicoechaniz): see if there's a more efficient way to build this recursive template data.
        link_template = Template(
            '{% if has_content %}'
              '<a href="{% url category-teaser_list slug %}">'
                 '<span>{{ name }}</span></a>'
            '{% else %} {{ name }}'
            '{% endif %}'
            ' <a href="{% url category_feed slug %}">'
            '<img src="{{ media_url }}images/css/rss_logo.png"/></a>'
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
                             'has_content': has_content,
                             'media_url':cyc_settings.CYCLOPE_THEME_MEDIA_URL,})))

        name = getattr(base_category, name_field)
        has_content = base_category.categorizations.exists()
        include = link_template.render(
            Context({'name': name,
                     'slug': base_category.slug,
                     'has_content': has_content,
                     'has_children': base_category.get_descendant_count(),
                     'media_url':cyc_settings.CYCLOPE_THEME_MEDIA_URL,}))
        if nested_list:
            return [include, nested_list]
        else:
            return [include]
frontend.site.register_view(Site, SiteMap)


class CommentsListOptions(forms.Form):
    limit_to_n_items = forms.IntegerField(label=_('Items to show'), min_value=1,
                                        initial=5,)


INLINE_CHOICES = (
    ("teaser", _(u"Teaser")),
    ("inline_detail", _(u"Detail")),
    ("labeled_icon", _(u"Labeled icons")),
)

class AuthorDetailOptions(forms.Form):
    show_authored_content = forms.BooleanField(label=_('Show authored content'),
                                               initial=True, required=False)
    inline_view_name = forms.ChoiceField(label=_('Inline type'),
                                         choices=INLINE_CHOICES,
                                         initial="teaser")
    items_per_page = forms.IntegerField(label=_('Items per page'), min_value=1,
                                        initial=cyc_settings.CYCLOPE_PAGINATION['TEASER'],)
    limit_to_n_items = forms.IntegerField(label=_('Limit to N items (0 = no limit)'),
                                          min_value=0, initial=0)
    sort_by = forms.ChoiceField(label=_('Sort by'),
                              choices=(("DATE-", _(u"Date ↓ (newest first)")),
                                       ("DATE+", _(u"Date ↑ (oldest first)")),
                                       ("ALPHABETIC", _(u"Alphabetic"))),
                              initial="DATE-")

class AuthoredMixin(object):

    options_form = AuthorDetailOptions

    def get_queryset(self, content_object):
        "Must return a queryset with all objects 'authored' by content_object"
        return NotImplementedError

    def get_page(self, request, req_context, options, content_object):
        from cyclope.core.collections.frontend_views import SORT_BY
        qs = self.get_queryset(content_object)

        sort_by = options["sort_by"]
        limit = options["limit_to_n_items"] or None
        sort_property, reverse, paginator_class = SORT_BY[sort_by]
        paginator_kwargs = {"per_page": options["items_per_page"]}
        if 'DATE' in sort_by:
            qs.sort(key=attrgetter(sort_property), reverse=reverse)
            if limit:
                qs = qs[:limit]
        elif 'ALPHABETIC' in sort_by:
            paginator_kwargs['on'] = "name"
        paginator = paginator_class(qs, **paginator_kwargs)
        page = cyclope.utils.get_page(paginator, request)
        return page


class AuthorDetail(AuthoredMixin, frontend.FrontendView):
    """Display an author's detail
    """
    name='detail'
    verbose_name=_('detailed view of the selected Author')
    is_default = True
    is_instance_view = True
    is_region_view = False
    is_content_view = True
    template = "cyclope/author_detail.html"

    def get_queryset(self, content_object):
        authored_content = []
        # get related methods like picture_set, article_set, etc.
        related = [attribute for attribute in dir(content_object) \
                   if attribute.endswith('_set')]
        for n in related:
            authored_content.extend(getattr(content_object, n).all())
        return authored_content

    def get_response(self, request, req_context, options, content_object):
        if options['show_authored_content']:
            authored_contents_page = self.get_page(request, req_context, options,
                                                   content_object)
        else:
            authored_contents_page = None

        return render_to_string(self.template, {
            'inline_view_name': options["inline_view_name"],
            'page': authored_contents_page
        }, req_context)


frontend.site.register_view(Author, AuthorDetail)

class SharingContentOptions(forms.Form):
    show_rss = forms.BooleanField(label=_('Show rss button'),
                                  initial=True, required=False)
    show_social_buttons = forms.BooleanField(label=_('Show social buttons'),
                                             initial=True, required=False,
                                             help_text="Display social buttons that are configured in SiteSettings")
    style = forms.ChoiceField(label=_('Style'),
                              choices=(("addthis_default_style", _(u"Horizontal small")),
                                       ("addthis_32x32_style addthis_default_style", _(u"Horizontal large")),
                                       ("addthis_vertical_style", _(u"Vertical small")),
                                       ("addthis_32x32_style addthis_vertical_style", _(u"Vertical large"))),
                              initial="addthis_default_style")

class SharingContent(frontend.FrontendView):

    """Display RSS and/or social network's follow buttons
    """
    name='share-content'
    verbose_name=_('sharing buttons')
    is_instance_view = False
    is_region_view = True
    is_content_view = False
    options_form = SharingContentOptions
    template = "cyclope/sharing_content.html"

    def get_response(self, request, req_context, options):

        return render_to_string(self.template, {
            'options': options,
        }, req_context)


frontend.site.register_view(Site, SharingContent)
