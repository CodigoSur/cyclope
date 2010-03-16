# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import ugettext as _
from django import forms
from django.db.models import get_model
from django.contrib.contenttypes import generic
from django.db import models

from mptt.forms import TreeNodeChoiceField
from feincms.admin import editor

from cyclope.widgets import WYMEditor
from models import *

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
    """
    Adds filtering by categories. To be used by Collectible based objects.
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
    description = forms.CharField(widget=WYMEditor(), required=False)
    parent = TreeNodeChoiceField(queryset=Category.tree.all(), required=False)

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
            'fields': ('active', 'description'),
        }),
    )

admin.site.register(Category, CategoryAdmin)


class CategoryMapForm(forms.ModelForm):
    # we need to declare this field in order to make it accessible from
    # CategoryMapInline through form.declared_fields and override the queryset
    category = TreeNodeChoiceField(queryset=None, required=True)

class CategoryMapInline(generic.GenericTabularInline):
    """
    Limits choices to those suitable for the content type
    of the object being created / changed
    """
    form = CategoryMapForm
    model = CategoryMap
    extra = 0

    def queryset(self, request):
        # we only override the queryset for the category field
        # this piece of code is here because we need it to be called when showing the form
        # it still looks like quite "hacky" a place to put it...
        req_app, req_model = request.path.rstrip('/').split('/')[-3:-1]
        req_model = models.get_model(req_app, req_model)
        req_model_ctype = ContentType.objects.get_for_model(req_model)

        qs = Category.tree.filter(collection__content_types=req_model_ctype)
        self.form.declared_fields['category'].queryset = \
            Category.tree.filter(collection__content_types=req_model_ctype)
        return super(CategoryMapInline, self).queryset(request)

class CollectibleAdmin (admin.ModelAdmin):
    """
    Base Admin model for Collectible based objects.
    """
    list_filter = ('categories',)
    inlines = [ CategoryMapInline, ]

admin.site.register(Collection)
