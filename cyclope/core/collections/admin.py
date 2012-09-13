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
core.collections.admin
----------------------
"""
import django
from django import forms
from django.contrib import admin
from django.db.models import get_model
from django.core.urlresolvers import reverse
from django.contrib.contenttypes import generic
from django.contrib.admin import SimpleListFilter
from django.utils.translation import ugettext_lazy as _

from markitup.widgets import AdminMarkItUpWidget
from mptt.forms import TreeNodeChoiceField
from mptt_tree_editor.admin import TreeEditor

from cyclope.core import frontend

from models import *
from cyclope.fields import MultipleField
from cyclope import settings as cyc_settings
from cyclope.core.perms.admin import CategoryPermissionInline
from cyclope.forms import ViewOptionsFormMixin
from cyclope.utils import PermanentFilterMixin

class CategoryListFilter(SimpleListFilter):
    title = _('category')
    parameter_name = 'categories__category__slug'

    def lookups(self, request, model_admin):
        # Lookups are arranged by collections in a collapsable way
        # so we add marks for the template (COLLECTION & EOCOLLECTION)
        object_ctype = ContentType.objects.get_for_model(model_admin.model)
        collections = Collection.objects.filter(content_types=object_ctype)
        lookup_choices = []
        for collection in collections:
            categories = Category.tree.filter(collection=collection)
            lookup_choices.append(("COLLECTION", collection.name))
            for category in categories:
                lookup_choices.append((category.slug, u'%s%s' % ('--'* category.level, category.name)))
            lookup_choices.append(("EOCOLLECTION", ""))
        return lookup_choices

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(categories__category__slug=self.value())


class CategoryForm(forms.ModelForm):
    description = forms.CharField(label=_('Description'),
                                  widget=AdminMarkItUpWidget(), required=False)
    parent = TreeNodeChoiceField(label=_('Parent'),
                                 queryset=Category.tree.all(), required=False)

    class Meta:
        model = Category


class CategoryAdmin(TreeEditor, PermanentFilterMixin):
    form = CategoryForm
    list_display = ("name", "thumbnail")
    list_filter = ['collection']
    fieldsets = (
        (None, {
            'fields': ('collection', 'name', 'parent')
        }),
        (_('Extra info'),{
            'classes': ('collapse',),
            'fields': ('slug', 'active', 'description', 'image',),
        }),
    )
    inlines = (CategoryPermissionInline,)
    permanent_filters = (
        (u"collection__id__exact",
         lambda request: unicode(Collection.objects.all()[0].id)),
    )

    def changelist_view(self, request, extra_context=None):
        self.do_permanent_filters(request)
        return super(CategoryAdmin, self).changelist_view(request, extra_context)

    class Media:
        js = (
            cyc_settings.CYCLOPE_STATIC_URL + 'js/reuse_django_jquery.js',
#            cyc_settings.CYCLOPE_STATIC_URL + 'js/jquery-ui-1.8.4.custom.min.js',
        )

admin.site.register(Category, CategoryAdmin)


class CategorizationForm(forms.ModelForm):
    # We declare these fields and override their querysets later.
    collection = forms.ModelChoiceField(
        label=_('Collection'),
        queryset=Collection.objects.all().order_by('-name'), required=False)
    category = TreeNodeChoiceField(label=_('Category'), queryset=None, required=True)

    def __init__(self, *args, **kwargs):
        super(CategorizationForm, self).__init__(*args, **kwargs)
        if self.instance.id is not None:
            self.fields['collection'].initial = self.instance.category.collection.pk


class CategorizationInline(generic.GenericStackedInline):
    """Limits choices to those suitable for the content type
    of the object being created / changed.
    """
    form = CategorizationForm
    model = Categorization
    extra = 0
    fieldsets = (
        (None, {
            'fields': ('collection', 'category',)
        }),
    )

    def queryset(self, request):
        # TODO(nicoechaniz):We only override the queryset for the category field.
        # This piece of code is here because we need it to be called
        # when showing the form. So __init__ can't be used
        # It still looks like quite "hacky" a place to put it...
        req_model_ctype = ContentType.objects.get_for_model(self.parent_model)

        self.form.base_fields['category'].queryset = \
            Category.tree.filter(
            collection__content_types=req_model_ctype).order_by('collection__name')

        self.form.base_fields['collection'].queryset = \
            Collection.objects.filter(
            content_types=req_model_ctype).order_by('name')

        return super(CategorizationInline, self).queryset(request)


class CollectibleAdmin(admin.ModelAdmin):
    """Base admin class for models that inherit from Collectible.
    """
    list_display = ("categories_on", )
    list_filter = (CategoryListFilter,)
    inlines = [CategorizationInline, ]
    valid_lookups = ('categories',)

    def categories_on(self, obj):
        category_list = [categzt.category for categzt in obj.categories.all()]
        template = ""
        for category in category_list:
            if template:
                template += ", "
            url = reverse("admin:collections_category_change", args=(category.pk,))
            template += '<a href="%s">%s</a>' % (url, category)
        return template

    categories_on.allow_tags = True
    categories_on.short_description = "Categories"

    def lookup_allowed(self, lookup, value=None):
        if lookup.startswith(self.valid_lookups):
            return True
        else:
            args = [lookup]
            if not django.VERSION[:3] == (1, 2, 4):
                args.append(value)
            return super(CollectibleAdmin, self).lookup_allowed(*args)


class CollectionAdminForm(forms.ModelForm, ViewOptionsFormMixin):
    raw_id_fields = ['picture',]
    default_list_view = forms.ChoiceField(label=_('Default category listing view'), required=False)
    view_options = MultipleField(label=_('View options'), form=None, required=False)

    options_field_name = 'view_options'
    view_field_name = 'default_list_view'
    field_names = ["default_list_view"]
    model = Category

    def __init__(self, *args, **kwargs):
        super(CollectionAdminForm, self).__init__(*args, **kwargs)
        self.fields['content_types'].choices = frontend.site.get_base_ctype_choices()
        model = get_model('collections', 'category')
        views = [('', '------')] + [ (view.name, view.verbose_name)
                                     for view in frontend.site.get_views(model)
                                     if view.name != 'default']
        self.fields['default_list_view'].choices = views
        self.model = model

        if self.instance.id is not None:
            self.set_initial_view_options(self.instance, self.instance)

    class Meta:
        model = Collection


class CollectionAdmin (admin.ModelAdmin):
    """Base admin class for models that inherit from Collectible.
    """
    form = CollectionAdminForm
    list_display = ["name", "thumbnail", "visible", "default_list_view"]
    list_editable = ("visible", )

admin.site.register(Collection, CollectionAdmin)
