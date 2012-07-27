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

from django.contrib import admin
from django import forms

from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.widgets import AdminTextareaWidget
from markitup.widgets import AdminMarkItUpWidget

from cyclope.core.collections.admin import CollectibleAdmin
from cyclope.admin import BaseContentAdmin
from cyclope.widgets import CKEditor
from cyclope.models import MenuItem
from cyclope import settings as cyc_settings
from cyclope.core import frontend
from models import StaticPage, HTMLBlock


class StaticPageAdminForm(forms.ModelForm):
    menu_items = forms.ModelMultipleChoiceField(label=_('Menu items'),
                    queryset = MenuItem.tree.all(), required=False,
                    )
    def __init__(self, *args, **kwargs):
    # this was initially written to be used for any BaseContent, that's
    # why we don't assume the content_type to be pre-determined
    # TODO(nicoechaniz): update code
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        if self.instance.id is not None:
            instance_type = ContentType.objects.get_for_model(self.instance)
            selected_items = [
                values[0] for values in
                MenuItem.objects.filter(
                    content_type=instance_type,
                    object_id=self.instance.id).values_list('id') ]
            self.fields['menu_items'].initial = selected_items

    class Meta:
        model = StaticPage


class StaticPageAdmin(CollectibleAdmin, BaseContentAdmin):
    # updates related menu_items information when a StaticPaget is saved
    form = StaticPageAdminForm
    list_display = ('__unicode__', ) + CollectibleAdmin.list_display
    search_fields = ('name', 'text', )
    fieldsets = ((None,
                  {'fields': ('name', 'text',)}),
                 (_('Publication data'),
                  {
                    'classes': ('collapse',),
                    'fields': ('published', 'summary', 'menu_items')}),
                 )
    inlines = CollectibleAdmin.inlines + BaseContentAdmin.inlines

    def save_model(self, request, obj, form, change):
        super(CollectibleAdmin, self).save_model(request, obj, form, change)
        object_type = ContentType.objects.get_for_model(obj)
        selected_items_ids = form.data.getlist('menu_items')
        selected_items = set(MenuItem.objects.filter(pk__in=selected_items_ids))
        old_items = set(MenuItem.objects.filter(content_type=object_type,
                                                object_id=obj.id))
        discarded_items = old_items.difference(selected_items)
        new_items = selected_items.difference(old_items)
        for menu_item in discarded_items:
            menu_item.content_type = None
            menu_item.object_id = None
            menu_item.content_view = None
            menu_item.save()
        for menu_item in new_items:
            menu_item.content_type = object_type
            menu_item.content_view = frontend.site.get_default_view_name(StaticPage)
            menu_item.object_id = obj.id
            menu_item.save()

admin.site.register(StaticPage, StaticPageAdmin)


class HTMLBlockAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(HTMLBlockAdminForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget = AdminTextareaWidget()


class HTMLBlockAdmin(admin.ModelAdmin):
    form = HTMLBlockAdminForm
    search_fields = ('name', 'text', )

admin.site.register(HTMLBlock, HTMLBlockAdmin)

