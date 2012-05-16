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
core.collections.models
-----------------------
Django models for generic categorization of content objects
"""

from operator import attrgetter

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db.models.signals import m2m_changed

import mptt
from autoslug.fields import AutoSlugField
from filebrowser.fields import FileBrowseField

import cyclope




class Collection(models.Model):
    """A facility for creating custom content collections.
    """

    name = models.CharField(_('name'), max_length=100, unique=True)
    slug = AutoSlugField(populate_from='name', always_update=True)
    # collections that aren't visible can be used to customize content behaviour
    visible = models.BooleanField(_('visible'),
                                             default=True)
    # the idea with navigation_root collections is that
    # URLS for these collections should be simplified. not used at the moment.
    navigation_root = models.BooleanField(_('navigation root'),
                                             default=False)
    content_types = models.ManyToManyField(ContentType, db_index=True,
                                           verbose_name=_('content types'))
    description = models.TextField(_('description'), blank=True, null=True)
    image =  FileBrowseField(_('image'), max_length=250, format='Image',
                             blank=True)
    default_list_view = models.CharField(_('default list view'), max_length=255,
                                    blank=True, default='')

    def get_absolute_url(self):
        return '/%s/%s/' % (self._meta.object_name.lower(), self.slug)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('collection')
        verbose_name_plural = _('collections')

def changed_ctypes(sender, instance, action, reverse, model, pk_set, **kwargs):
    ## we remove previous categorizations that were set for content types
    ## that are no longer accepted by the collection
    if action == 'post_add' and pk_set:
        Categorization = models.get_model('collections', 'categorization')
        cats = Categorization.objects.filter(
            category__collection=instance).exclude(content_type__pk__in=pk_set).delete()

m2m_changed.connect(changed_ctypes, sender=Collection.content_types.through)


class Category(models.Model):
    """Categories are associated with a specific Collection,
    and can be generically usable with any content type.
    """

    collection = models.ForeignKey(Collection,
        verbose_name=_('collection'), related_name='categories')
    name = models.CharField(_('name'), max_length=100)
    slug = AutoSlugField(populate_from='name', unique=True,
                         db_index=True, always_update=True)
#    slug = AutoSlugField(populate_from='name', always_update=True)
#                         unique_with=('parent', 'collection'))
    parent = models.ForeignKey('self', verbose_name=_('parent'),
                              related_name='children', null=True, blank=True)
    active = models.BooleanField(_('active'), default=True, db_index=True)
    description = models.TextField(_('description'), blank=True, null=True)
    image =  FileBrowseField(_('image'), max_length=250, format='Image',
                             blank=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return '/%s/%s/' % (self._meta.object_name.lower(), self.slug)

    def valid_parents(self):
        return Category.tree.filter(pk__isnot=self.pk)

    def save(self, moving_childs=False, *args, **kwargs):
        # If is not a new Category and the Collection is changed, we move all
        # childrens to the new Collection adding the necesary content_types to
        # the new collection.
        if self.pk is not None:
            old_category = Category.objects.get(pk=self.pk)
            if old_category.collection != self.collection:
                # If we are moving a non root category it must be root in
                # the new collection
                if self.is_child_node() and not moving_childs:
                    self.parent = None
                # Add the content_types of the categorizations to new collection
                descendants = old_category.get_descendants()
                all_categories = [self] + list(descendants)
                categorizations_list = Categorization.objects.filter(category__in=all_categories)
                content_types = list(set([cat.content_type for cat in categorizations_list]))
                self.collection.content_types.add(*content_types)

                for child in descendants:
                    child.collection = self.collection
                    child.save(moving_childs=True)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        unique_together = ('collection', 'name')
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        get_latest_by = "pk"

mptt.register(Category)


class CategorizationManager(models.Manager):

    def get_for_object(self, obj):
        """Get all Categorizations for an instance of a content object.

        Args:
          obj: a model or instance
        """

        ctype = ContentType.objects.get_for_model(obj)
        return self.filter(content_type__pk=ctype.pk, object_id=obj.pk)

    def get_for_ctype(self, ctype):
        """Get all Categorizations available for this content_type.

        Args:
          ctype: a ContentType instance
        """
        return self.filter(content_type__pk=ctype.pk)

    def get_for_category(self, category, sort_property='name', limit=None,
                         traverse_children=False, reverse=False):
        if traverse_children:
            categories = [category]+list(category.get_descendants())
        else:
            categories = [category]

        collection_models = [ct.model_class() for ct in categories[0].collection.content_types.all()]
        categorizations_list = []
        for content_model in collection_models:
            sql_params = {
                    'content_model_tbl': content_model._meta.db_table,
                    'content_type': ContentType.objects.get_for_model(content_model).id,
                    'categorization_tbl': Categorization._meta.db_table,
                    'category_tbl': Category._meta.db_table,
                    'category_ids': ', '.join([ str(category.id) for category in categories ]),
                    'sort_property': sort_property
                }

            categorization_query = \
                'SELECT collections_categorization.*, %(content_model_tbl)s.%(sort_property)s AS sort_property FROM  collections_categorization '\
                'JOIN %(content_model_tbl)s ON %(content_model_tbl)s.id = collections_categorization.object_id '\
                'AND %(content_type)s = collections_categorization.content_type_id '\
                'JOIN %(category_tbl)s ON %(category_tbl)s.id = collections_categorization.category_id '\
                'WHERE  %(category_tbl)s.id IN (%(category_ids)s) '\
                'GROUP BY collections_categorization.object_id' % sql_params

            ##TODO(nicoechaniz): replace string formating with params list. reference http://docs.djangoproject.com/en/dev/topics/db/sql/
            categorizations_list += Categorization.objects.raw(categorization_query)

        ##TODO(nicoechaniz): we should get all data in one query and properly sorted
        return sorted(categorizations_list, key=attrgetter('sort_property'), reverse=reverse)[slice(limit)]


class Categorization(models.Model):
    """Represents the association of a catergory and a content object."""

    category = models.ForeignKey('Category', verbose_name=_('category'),
                                 db_index=True, related_name='categorizations')
    content_type = models.ForeignKey(ContentType, db_index=True,
                                     verbose_name=_('content type'))
    object_id = models.PositiveIntegerField(db_index=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    objects = CategorizationManager()

    @property
    def object_modification_date(self):
        return self.content_object.modification_date

    @property
    def object_creation_date(self):
        return self.content_object.creation_date

    def __unicode__(self):
        return '%(collection_name)s: %(category_name)s' % {
            'collection_name': self.category.collection.name,
            'category_name': self.category.name}

    class Meta:
        verbose_name = _('categorization')
        verbose_name_plural = _('categorizations')
#        ordering = ('object_modification_date',)


class Collectible(models.Model):
    """Base class for collectible objects
    """
    categories = generic.GenericRelation('Categorization',
        content_type_field='content_type', object_id_field='object_id',
        verbose_name = _('categories'))

    # activate custom admin filter
    categories.category_filter = True

    def is_orphan(self):
        return not self.categories.exists()
    is_orphan.short_description = _('is orphan')

    class Meta:
        abstract = True
