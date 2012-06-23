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
admin
-----
configuration for the Django admin
"""

from django.db import models
from django.contrib import admin
from django.core import urlresolvers
from django.contrib.admin.options import FORMFIELD_FOR_DBFIELD_DEFAULTS
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.comments.admin import CommentsAdmin
from django.http import HttpResponseRedirect

from feincms.admin import editor

from cyclope.models import *
from cyclope.forms import MenuItemAdminForm,\
                          SiteSettingsAdminForm,\
                          LayoutAdminForm,\
                          RegionViewInlineForm,\
                          RelatedContentForm,\
                          AuthorAdminForm

from cyclope.widgets import get_default_text_widget
from cyclope.core.collections.admin import CollectibleAdmin
import cyclope.settings as cyc_settings


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
        return super(UserAdmin, self).response_add(request, obj, post_url_continue)


        
from django.utils.functional import update_wrapper

class MenuItemAdmin(editor.TreeEditor):
    form = MenuItemAdminForm
    fieldsets = ((None,
                  {'fields': ('menu', 'parent', 'name', 'site_home', 'active')}),
                 (_('content details'),
                  {'fields':('custom_url', 'content_type', 'content_view',
                             'view_options', 'object_id'),
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


    def changelist_view(self, request, extra_context=None):
        # menuitems changelist should only show items from one menu.
        # so we activate the filter to display main menu items when no filters
        # have been selected by the user
        if Menu.objects.count():
            main_menu =  Menu.objects.get(main_menu=True)
            if main_menu:
                menu_id = main_menu.id
            else:
                menu_id = Menu.objects.all()[0].id
            if not request.GET:
                request.GET = {u'menu__id__exact': unicode(menu_id)}
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

admin.site.register(SiteSettings, SiteSettingsAdmin)

class ImageAdmin(admin.ModelAdmin):
	list_display = ['thumbnail']

admin.site.register(Image, ImageAdmin)

class AuthorAdmin(admin.ModelAdmin):
    form = AuthorAdminForm
    search_fields = ('name', 'origin', 'notes')

admin.site.register(Author, AuthorAdmin)

admin.site.register(Source)

class CyclopeCommentsAdmin(CommentsAdmin):
    fieldsets = (
        (None,
           {'fields': ('content_type', 'object_pk')}
        ),
        (_('Content'),
           {'fields': ('user', 'user_name', 'user_email', 'user_url', 'comment')}
        ),
        (_('Metadata'),
           {'fields': ('submit_date', 'ip_address', 'is_public', 'is_removed')}
        ),
     )
    list_display = ('name', "content", "content_url", 'content_type', 'ip_address',
                    'submit_date', 'is_public', 'is_removed')
    list_filter = ('submit_date', 'is_public', 'is_removed')

    def content(self, obj):
        admin_url_name = "%s_%s_change" % (obj.content_type.app_label, obj.content_type.name)
        admin_url_name = admin_url_name.replace(" ", "")
        change_url = urlresolvers.reverse('admin:%s' % admin_url_name, args=(obj.content_object.id,))
        return "<a href='%s'>%s</a>" % (change_url, obj.content_object)
    content.allow_tags = True

    def content_url(self, obj):
        url = obj.content_object.get_absolute_url()
        return  "<a href='%s'>%s</a>" % (url, url)
    content_url.allow_tags = True


admin.site.unregister(Comment)
admin.site.register(Comment, CyclopeCommentsAdmin)
