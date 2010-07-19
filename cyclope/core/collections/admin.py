# -*- coding: utf-8 -*-
"""
core.collections.admin
----------------------
"""

from django.contrib import admin
from django.utils.translation import ugettext as _
from django import forms
from django.db.models import get_model
from django.contrib.contenttypes import generic
from django.db import models

from mptt.forms import TreeNodeChoiceField
from feincms.admin import editor

from cyclope.widgets import WYMEditor
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

    def __init__(self, f, request, params, model, model_admin):
        super(CategoryFilterSpec, self).__init__(f, request, params, model,
                                                   model_admin)

        self.lookup_kwarg = 'categories__category__slug'
        self.lookup_val = request.GET.get(self.lookup_kwarg, None)

        object_ctype = ContentType.objects.get_for_model(model)

        # select categories available for the content type of the object
        qs = Category.tree.filter(collection__content_types=object_ctype)
        # create list of choices and the corresponding indented labels
        self.lookup_choices = [(item.slug, u'%s%s' % \
                                ('-'* item.level, item.name)) \
                                for item in qs ]
        self.model = model

    def choices(self, cl):
        # show All items when no choice is selected
        yield {'selected': self.lookup_val is None,
                'query_string': cl.get_query_string({}, [self.lookup_kwarg]),
                'display': _('All')}
        for [val, display] in self.lookup_choices:
            yield {'selected': smart_unicode(val) == self.lookup_val,
                  'query_string': cl.get_query_string({self.lookup_kwarg: val}),
                  'display': display}

    def title(self):
        return _('%s categories' % self.model._meta.verbose_name)

FilterSpec.filter_specs.insert(0, (lambda f: \
                                   getattr(f, 'category_filter', False),
                                   CategoryFilterSpec))
####


class CategoryForm(forms.ModelForm):
    description = forms.CharField(label=_('Description'),
                                  widget=WYMEditor(), required=False)
    parent = TreeNodeChoiceField(label=_('Parent'),
                                 queryset=Category.tree.all(), required=False)

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

admin.site.register(Category, CategoryAdmin)


class CategoryMapForm(forms.ModelForm):
    # We declare these fields and override their querysets later.
    collection = forms.ModelChoiceField(
        label=_('Collection'),
        queryset=Collection.objects.all().order_by('-name'), required=False)
    category = TreeNodeChoiceField(label=_('Category'), queryset=None, required=True)

    def __init__(self, *args, **kwargs):
        super(CategoryMapForm, self).__init__(*args, **kwargs)
        if self.instance.id is not None:
            self.fields['collection'].initial = self.instance.category.collection.pk


class CategoryMapInline(generic.GenericStackedInline):
    """Limits choices to those suitable for the content type
    of the object being created / changed.
    """
    form = CategoryMapForm
    model = CategoryMap
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

        return super(CategoryMapInline, self).queryset(request)


class CollectibleAdmin (admin.ModelAdmin):
    """Base admin class for models that inherit from Collectible.
    """
    list_filter = ('categories',)
    inlines = [ CategoryMapInline, ]


class CollectionAdminForm(forms.ModelForm):
    raw_id_fields = ['picture',]

    def __init__(self, *args, **kwargs):
        super(CollectionAdminForm, self).__init__(*args, **kwargs)
        ctype_choices = [('', '------')]
        for model in frontend.site._registry:
            if model not in [Category, Collection, Menu]:
                ctype = ContentType.objects.get_for_model(model)
                ctype_choices.append((ctype.id, model._meta.verbose_name))
        self.fields['content_types'].choices = ctype_choices

    class Meta:
        model = Collection

class CollectionAdmin (admin.ModelAdmin):
    """Base admin class for models that inherit from Collectible.
    """
    form = CollectionAdminForm

admin.site.register(Collection, CollectionAdmin)
