#!/usr/bin/env python
# -*- coding: UTF-8 -*-
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

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
import mptt
from autoslug.fields import AutoSlugField
from filebrowser.fields import FileBrowseField


class Collection(models.Model):
    """A facility for creating custom content collections.
    """

    name = models.CharField(_('name'), max_length=50, unique=True)
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

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('collection')
        verbose_name_plural = _('collections')


class Category(models.Model):
    """Categories are associated with a specific Collection,
    and can be generically usable with any content type.
    """

    collection = models.ForeignKey(Collection,
        verbose_name=_('collection'), related_name=_('collection categories'))
    name = models.CharField(_('name'), max_length=50)
    slug = AutoSlugField(populate_from='name', always_update=True,
                         unique_with=('parent', 'collection'))
    parent = models.ForeignKey('self', verbose_name=_('parent'),
                              related_name=_('children'), null=True, blank=True)
    active = models.BooleanField(_('active'), default=True, db_index=True)
    description = models.TextField(_('description'), blank=True, null=True)
    image =  FileBrowseField(_('image'), max_length=250, format='Image',
                             blank=True)

    def __unicode__(self):
        return self.name

  # this is needed for the feincms.editor.TreeEditor to correctly display the hierarchy
    def get_absolute_url(self):
        return self.__unicode__()


    def valid_parents(self):
        return Category.tree.filter(pk__isnot=self.pk)

    def get_instance_url(self, view_name=None):
        view = get_view(self.__class__, view_name)

        if view.is_default:
            return '%s/%s'\
                    % (self._meta.object_name.lower(),
                       self.slug)

        if view.is_instance_view:
            return '%s/%s/View/%s'\
                    % (self._meta.object_name.lower(),
                       self.slug, view_name)
        else:
            return '%s/View/%s'\
                    % (self._meta.object_name.lower(), view_name)

    class Meta:
        unique_together = ('collection', 'name')
        verbose_name = _('category')
        verbose_name_plural = _('categories')

mptt.register(Category)


class CategoryMapManager(models.Manager):

    def get_for_object(self, obj):
        """Get all Category Maps for an instance of a content object.

        Args:
          obj: a model or instance
        """

        ctype = ContentType.objects.get_for_model(obj)
        return self.filter(content_type__pk=ctype.pk, object_id=obj.pk)

    def get_for_ctype(self, ctype):
        """Get all Collection Categories available for this content_type.

        Args:
          ctype: a ContentType instance
        """
        return self.filter(content_type__pk=ctype.pk)


class CategoryMap(models.Model):
    """Mappings between a content object and it's associated categories."""

    category = models.ForeignKey('Category', verbose_name=_('category'),
                                 db_index=True, related_name='category_maps')
    content_type = models.ForeignKey(ContentType, db_index=True,
                                     verbose_name=_('content type'))
    object_id = models.PositiveIntegerField(db_index=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    objects = CategoryMapManager()

    def __unicode__(self):
        return '%(collection_name)s: %(category_name)s' % {
            'collection_name': self.category.collection.name,
            'category_name': self.category.name}

    class Meta:
        verbose_name = _('category map')
        verbose_name_plural = _('category maps')


class Collectible(models.Model):
    """Base class for collectible objects
    """
    categories = generic.GenericRelation('CategoryMap',
        content_type_field='content_type', object_id_field='object_id',
        verbose_name = _('categories'))

    # activate custom admin filter
    categories.category_filter = True

    @property
    def is_orphan(self):
        return not self.categories.exists()

    class Meta:
        abstract = True
