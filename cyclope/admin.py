# -*- coding: utf-8 -*-
"""
admin
-----
configuration for the Django admin
"""

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType

from feincms.admin import editor

from cyclope.models import *
from cyclope.forms import MenuItemAdminForm,\
                          SiteSettingsAdminForm,\
                          LayoutAdminForm,\
                          RegionViewInlineForm,\
                          RelatedContentForm
from cyclope.core.collections.admin import CollectibleAdmin


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

class MenuItemAdmin(editor.TreeEditor):
    form = MenuItemAdminForm
    fieldsets = ((None,
                  {'fields': ('menu', 'parent', 'name', 'site_home', 'custom_url',
                              'layout', 'active')}),
                 (_('content details'),
                  {
#                    'classes': ('collapse',),
                  'fields':('content_type', 'content_view', 'object_id')})
                )
    list_filter = ('menu',)

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
