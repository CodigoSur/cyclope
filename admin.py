# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import ugettext as _
from feincms.admin import editor

from cyclope.models import *
from cyclope.forms import StaticPageAdminForm,\
                          MenuItemAdminForm,\
                          BaseContentAdminForm,\
                          SiteSettingsAdminForm,\
                          LayoutAdminForm,\
                          RegionViewInlineForm
from cyclope.core.collections.admin import CollectibleAdmin

#class MenuItemInline(admin.TabularInline):
#    """
#    """
#    model=MenuItem
#    extra = 0


#class BaseContentAdmin(admin.ModelAdmin):
#    """
#    """
#    #form = BaseContentAdminForm
#    #def save_model(self, request, obj, form, change):
#    #    for id in form.data.getlist('menu_items'):
#    #        menu_item = MenuItem.objects.get(pk=id)
#    #        menu_item.content_object = obj
#    #        menu_item.save()
#    #    super(BaseContentAdmin, self).save_model(request, obj, form, change)
#
#    inlines = []
##    inlines = [ MenuItemInline, ]

class MenuItemAdmin(editor.TreeEditor):
    form = MenuItemAdminForm
#    readonly_fields = ['content_object']
    raw_id_fields = ['content_object']
    fieldsets = ((None,
                  {'fields': ('menu', 'parent', 'name', 'custom_url', 'active')}),
                 (_('content details'),
                  {'classes': ('collapse',),
                  'fields':('layout', 'content_type', 'content_object', 'content_view')})
                )
    list_filter = ('menu',)

admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(Menu)
admin.site.register(BaseContent)

from django import forms
from cyclope.widgets import WYMEditor

class StaticPageAdmin(CollectibleAdmin):
    form = StaticPageAdminForm

admin.site.register(StaticPage, StaticPageAdmin)

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

#admin.site.register(BlockView)
