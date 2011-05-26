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
core.collections.admin
----------------------
"""
import django
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.db.models import get_model
from django.contrib.contenttypes import generic
from django.db import models

from markitup.widgets import AdminMarkItUpWidget
from mptt.forms import TreeNodeChoiceField
from feincms.admin import editor

#from cyclope.widgets import CKEditor

from cyclope.core import frontend

from models import *
from cyclope.models import Menu
from cyclope import settings as cyc_settings

####
# custom FilterSpec
# based on snippet found at:
# http://www.djangosnippets.org/snippets/1051/
# This is a workaround to add a custom filter to the admin changelist
# until a generic way of adding custom filter specs make it into django.
# See ticket: http://code.djangoproject.com/ticket/5833
####

from django.db import models
from django.contrib.admin.filterspecs import FilterSpec, ChoicesFilterSpec
from django.utils.encoding import smart_unicode

class CategoryFilterSpec(ChoicesFilterSpec):
    """Adds filtering by categories.

    To be used by Collectible based objects.

    categories.category_filter must be set to True in the model
    for this filter to be active.
    """
    def __init__(self, f, request, params, model, model_admin, field_path=None):
        super(CategoryFilterSpec, self).__init__(f, request, params, model,
                                                   model_admin, field_path)

        self.lookup_kwarg = 'categories__category__slug'
        self.lookup_val = request.GET.get(self.lookup_kwarg, None)

        object_ctype = ContentType.objects.get_for_model(model)
        collections = Collection.objects.filter(content_types=object_ctype)

        self.lookup_choices = []
        for collection in collections:
            # we hack a bit on the standard django way of displaying filters
            # to allow for a collapsible sub-level
            self.lookup_choices.append(
                (None, "</a><div><span class='expand_collapse'>"+collection.name+"</span><ul class='categories-filter'>"))
            categories = Category.tree.filter(collection=collection)
            for category in categories:
                self.lookup_choices.append((category.slug, u'%s%s' % \
                                            ('--'* category.level, category.name)))
            self.lookup_choices.append((None, "</a></ul></div>"))

        self.model = model

    def choices(self, cl):
        # show All items when no choice is selected
        yield {'selected': self.lookup_val is None,
                'query_string': cl.get_query_string({}, [self.lookup_kwarg]),
                'display': _('All')}
        for [val, display] in self.lookup_choices:
            selected = smart_unicode(val) == self.lookup_val
            if selected:
                display = display.lstrip('-')
            yield {'selected': selected,
                  'query_string': cl.get_query_string({self.lookup_kwarg: val}),
                  'display': display}

    def title(self):
        return _('categories')

FilterSpec.filter_specs.insert(0, (lambda f: \
                                   getattr(f, 'category_filter', False),
                                   CategoryFilterSpec))
####


class CategoryForm(forms.ModelForm):
    description = forms.CharField(label=_('Description'),
                                  widget=AdminMarkItUpWidget(), required=False)
    parent = TreeNodeChoiceField(label=_('Parent'),
                                 queryset=Category.tree.all(), required=False)

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        if self.instance.id is not None:
            current_col = self.instance.collection
            self.fields['collection'].choices = [(current_col.pk, current_col)]

    class Meta:
        model = Category

class CategoryAdmin(editor.TreeEditor):
    form = CategoryForm
    list_filter = ['collection']
    fieldsets = (
        (None, {
            'fields': ('collection', 'name', 'parent')
        }),
        (_('Extra info'),{
            'classes': ('collapse',),
            'fields': ('active', 'description', 'image',),
        }),
    )
    def changelist_view(self, request, extra_context=None):
        # category changelist should only show items from one collection.
        # so we activate the filter to display categories from one collection
        # when no filters have been selected by the user
        a_collection = Collection.objects.all()[0].id
        if not request.GET:
            request.GET = {u'collection__id__exact': unicode(a_collection)}
        return super(CategoryAdmin, self).changelist_view(request, extra_context)


    class Media:
        js = (
            cyc_settings.CYCLOPE_MEDIA_URL + 'js/reuse_django_jquery.js',
#            cyc_settings.CYCLOPE_MEDIA_URL + 'js/jquery-ui-1.8.4.custom.min.js',
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


class CollectibleAdmin (admin.ModelAdmin):
    """Base admin class for models that inherit from Collectible.
    """
    list_filter = ('categories',)
    inlines = [ CategorizationInline, ]
    valid_lookups = ('categories',)

    def lookup_allowed(self, lookup, value=None):
        if lookup.startswith(self.valid_lookups):
            return True
        else:
            args = [lookup]
            if not django.VERSION[:3] == (1, 2, 4):
                args.append(value)
            return super(CollectibleAdmin, self).lookup_allowed(*args)


class CollectionAdminForm(forms.ModelForm):
    raw_id_fields = ['picture',]
    default_list_view = forms.ChoiceField(label=_('Default category listing view'), required=False)

    def __init__(self, *args, **kwargs):
        super(CollectionAdminForm, self).__init__(*args, **kwargs)
        self.fields['content_types'].choices = frontend.site.get_base_ctype_choices()
        model = get_model('collections', 'category')
        views = [('', '------')] + [ (view.name, view.verbose_name)
                                     for view in frontend.site._registry[model]
                                     if view.name != 'default']
        self.fields['default_list_view'].choices = views

    class Meta:
        model = Collection

class CollectionAdmin (admin.ModelAdmin):
    """Base admin class for models that inherit from Collectible.
    """
    form = CollectionAdminForm

admin.site.register(Collection, CollectionAdmin)
