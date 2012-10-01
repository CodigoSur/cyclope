#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010-2012 Código Sur Sociedad Civil.
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
admin
-----
configuration for the Django admin
"""

from django.db import models
from django.contrib import admin
from django.core import urlresolvers
from django.contrib.admin.options import FORMFIELD_FOR_DBFIELD_DEFAULTS
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect
from django.contrib.sites.models import Site

from mptt_tree_editor.admin import TreeEditor

from cyclope.models import *
from cyclope.forms import MenuItemAdminForm,\
                          SiteSettingsAdminForm,\
                          LayoutAdminForm,\
                          RegionViewInlineForm,\
                          RelatedContentForm,\
                          AuthorAdminForm

from cyclope.widgets import get_default_text_widget
from cyclope.core.collections.admin import CollectibleAdmin
from cyclope.core.collections.models import Category
import cyclope.settings as cyc_settings
from cyclope.utils import PermanentFilterMixin

# Set default widget for all admin textareas
default_admin_textfield = FORMFIELD_FOR_DBFIELD_DEFAULTS[models.TextField]
default_admin_textfield['widget'] = get_default_text_widget()

class RelatedContentInline(generic.GenericStackedInline):
    form = RelatedContentForm
    ct_field = 'self_type'
    ct_fk_field = 'self_id'
    model = RelatedContent
    extra = 0


class BaseContentAdmin(admin.ModelAdmin):
    """Base class for content models to use instead of admin.ModelAdmin
    """
    inlines = [RelatedContentInline]
    date_hierarchy = 'creation_date'

    class Media:
        js = (
            cyc_settings.CYCLOPE_STATIC_URL + 'js/reuse_django_jquery.js',
            cyc_settings.CYCLOPE_STATIC_URL + 'js/jquery-ui-1.8.4.custom.min.js',
        )

    def response_change(self, request, obj):
        if '_frontend' in request.REQUEST:
            return HttpResponseRedirect(obj.get_absolute_url())
        return super(BaseContentAdmin, self).response_change(request, obj)

    def response_add(self, request, obj, post_url_continue='../%s/'):
        if '_frontend' in request.REQUEST:
            return HttpResponseRedirect(obj.get_absolute_url())
        return super(BaseContentAdmin, self).response_add(request, obj, post_url_continue)

    def has_delete_permission(self, request, obj=None):
        # this is redundant with _popup, which already sets delete_permission to False
        if '_frontend' in request.REQUEST:
            return False
        return super(BaseContentAdmin, self).has_delete_permission(request, obj)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        if '_frontend' in request.REQUEST:
            if extra_context is None:
                extra_context = {}
            extra_context['frontend_admin'] = 'frontend_admin'

        return super(BaseContentAdmin, self).change_view(request, object_id,
                                                          form_url, extra_context)

    def add_view(self, request, form_url='', extra_context=None):
        if '_frontend' in request.REQUEST:
            if extra_context is None:
                extra_context = {}
            extra_context['frontend_admin'] = 'frontend_admin'
        if '_from_category' in request.REQUEST:
            ## TODO(nicoechaniz): this could be used to set the categorization, but is not implemented yet
            category_slug = request.REQUEST['_from_category']
            category = Category.objects.get(slug=category_slug)
            extra_context['initial_category'] = category.id
            extra_context['initial_collection'] = category.collection.id
        return super(BaseContentAdmin, self).add_view(request, form_url, extra_context)

    def save_model(self, request, obj, form, change):
        # sets the user as the creator of the content
        if getattr(obj, 'user', None) is None:
            obj.user = request.user
        obj.save()


class MenuItemAdmin(TreeEditor, PermanentFilterMixin):
    form = MenuItemAdminForm
    fieldsets = ((None,
                  {'fields': ('menu', 'parent', 'name', 'slug', 'site_home', 'active')}),
                 (_('content details'),
                  {'fields':('custom_url', 'content_type', 'content_view',
                             'view_options', 'content_object',),
                  'description': _(u"Either set an URL here or select a content"
                                    "type and view.")
                  }),
                 (_('layout'),
                  {'fields':('layout', 'persistent_layout'),
                   'classes': ('collapse',),
                   'description': _(u"Set the layout that will be used when this "
                                    "menuitem is selected.")
                   }),
                )
    list_filter = ('menu',)

    permanent_filters = (
        (u"menu__id__exact",
         lambda request: unicode(Menu.objects.all()[0].id)),
    )

    def changelist_view(self, request, extra_context=None):
        self.do_permanent_filters(request)
        return super(MenuItemAdmin, self).changelist_view(request, extra_context)

admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(Menu)


class RegionViewInline(admin.StackedInline):
    form = RegionViewInlineForm
    model = RegionView
    extra = 1


class LayoutAdmin(admin.ModelAdmin):
    form = LayoutAdminForm
    inlines = (RegionViewInline, )

admin.site.register(Layout, LayoutAdmin)


class SiteSettingsAdmin(admin.ModelAdmin):
    form = SiteSettingsAdminForm

    def has_add_permission(self, request):
        """ Prevent addition of new objects """
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(SiteSettings, SiteSettingsAdmin)

class ImageAdmin(admin.ModelAdmin):
    list_display = ['thumbnail']

admin.site.register(Image, ImageAdmin)

class AuthorAdmin(admin.ModelAdmin):
    form = AuthorAdminForm
    list_display = ('name', 'thumbnail')
    search_fields = ('name', 'origin', 'notes')

admin.site.register(Author, AuthorAdmin)

admin.site.register(Source)

class SiteAdmin(admin.ModelAdmin):
    list_display = ('domain', 'name')
    search_fields = ('domain', 'name')

    def has_add_permission(self, request):
        """ Prevent addition of new objects """
        return False

    def has_delete_permission(self, request, obj=None):
        return False



import django.contrib.sites.admin # Force register of django's SiteAdmin
admin.site.unregister(Site)
admin.site.register(Site, SiteAdmin)
