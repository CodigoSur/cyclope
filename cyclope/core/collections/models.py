#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010-2013 Código Sur Sociedad Civil.
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
import random
from operator import attrgetter
from collections import defaultdict

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db.models.signals import m2m_changed

import mptt
from jsonfield import JSONField
from autoslug.fields import AutoSlugField
from filebrowser.fields import FileBrowseField

import cyclope
from cyclope.utils import ThumbnailMixin

class Collection(models.Model, ThumbnailMixin):
    """A facility for creating custom content collections.
    """

    name = models.CharField(_('name'), max_length=100, unique=True)
    slug = AutoSlugField(populate_from='name', always_update=False,
                         editable=True, blank=True)
    # collections that aren't visible can be used to customize content behaviour
    visible = models.BooleanField(_('visible'), default=True)
    # TODO the idea with navigation_root collections is that
    # URLS for these collections should be simplified. not used at the moment.
    navigation_root = models.BooleanField(_('navigation root'), default=False)
    content_types = models.ManyToManyField(ContentType, db_index=True,
                                           verbose_name=_('content types'))
    description = models.TextField(_('description'), blank=True, null=True)
    image =  FileBrowseField(_('image'), max_length=250, format='Image',
                             blank=True)
    default_list_view = models.CharField(_('default list view'), max_length=255,
                                         blank=True, default='')
    view_options = JSONField(default='{}') # default is taken from ViewOptionsForm

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

class Category(models.Model, ThumbnailMixin):
    """Categories are associated with a specific Collection,
    and can be generically usable with any content type.
    """

    collection = models.ForeignKey(Collection,
        verbose_name=_('collection'), related_name='categories')
    name = models.CharField(_('name'), max_length=100)
    slug = AutoSlugField(populate_from='name', unique=True, db_index=True,
                         always_update=False, editable=True, blank=True)
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


def dictfetchall(cursor): 
    "Returns all rows from a cursor as a dict" 
    desc = cursor.description 
    return [
        dict(zip([col[0] for col in desc], row)) 
        for row in cursor.fetchall() 
    ]

class CategorizationManager(models.Manager):

    def _content_in_categories(self, q):
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute( q )
        result_list = []
        for row in dictfetchall(cursor):
            num_cat = row.pop("num_cat", None)
            cat = self.model(**row)
            if num_cat: cat.num_cat = num_cat
            result_list.append(cat)
        return result_list

# These queries are not ANSI SQL standard, backticks are MySQL specific although Sqlite accepts them.
# Might be better to change backticks for double quotes. MySQL should then be set to use ANSI:
# SET GLOBAL SQL_MODE=ANSI_QUOTES; for the queries to work properly
    def content_object_in_all(self, categories):
        category_ids = ",".join([ str(category.id) for category in categories ])
        q = """
        SELECT *, COUNT(collections_categorization.category_id) AS num_cat FROM collections_categorization WHERE (collections_categorization.category_id IN (%s)) GROUP BY collections_categorization.content_type_id, collections_categorization.object_id HAVING COUNT(collections_categorization.category_id) = %s  ORDER BY `collections_categorization`.`order` ASC, `collections_categorization`.`id` DESC
        """ % (category_ids, len(categories))
        return self._content_in_categories(q)

    def content_object_in_any(self, categories):
        category_ids = ",".join([ str(category.id) for category in categories ])
        q = """
        SELECT * FROM collections_categorization WHERE (collections_categorization.category_id IN (%s)) GROUP BY collections_categorization.content_type_id, collections_categorization.object_id ORDER BY `collections_categorization`.`order` ASC, `collections_categorization`.`id` DESC
        """ % category_ids
        return self._content_in_categories(q)

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

    def get_for_category(self, category, sort_property="name", limit=None,
                         traverse_children=False, reverse=False, intersection=False):

        try:
            categories = list(category)
        except:
            categories = [category]

        if traverse_children:
            # TODO(nicoechaniz): fix (intersection==True and get_descendants==True) case
            # then enable traverse_children option in CategoryFilteredList view
            # and remove intersection = False here
            intersection = False
            for cat in categories:
                categories += list(cat.get_descendants())

        if intersection:
            cats = Categorization.objects.content_object_in_all(categories)
        else:
            cats = Categorization.objects.content_object_in_any(categories)

        if sort_property == "random":
            cats = list(cats)
            random.shuffle(cats)
        elif sort_property == "creation_date":
            # the default ordering is reversed
            if not reverse:
                cats = cats.reverse()
        else: # sort by name
            ct_vals = defaultdict(list)
            for cat in cats:
                ct_vals[cat.content_type_id].append(cat.object_id)
            # Iterate over content_types fetching the sort_key of the content_object and saving in sort_attrs dict
            sort_attrs = {}
            def chunks(l, n):
                """ Yield successive n-sized chunks from l.
                """
                for i in xrange(0, len(l), n):
                    yield l[i:i+n]
            for ct_id, object_ids in ct_vals.iteritems():
                ct = ContentType.objects.get_for_id(ct_id)
                for object_ids in chunks(object_ids, 450):
                    for obj_id, val in ct.get_all_objects_for_this_type(pk__in=object_ids).values_list("pk", sort_property):
                        sort_attrs[(ct_id, obj_id)] = val

            cats = sorted(cats, key=lambda c: sort_attrs[(c.content_type_id, c.object_id)],
                          reverse=reverse)
        if cats:
            return cats[slice(limit)]
        else:
            return Categorization.objects.none()


class Categorization(models.Model):
    """Represents the association of a catergory and a content object."""

    category = models.ForeignKey('Category', verbose_name=_('category'),
                                 db_index=True, related_name='categorizations')
    content_type = models.ForeignKey(ContentType, db_index=True,
                                     verbose_name=_('content type'))
    object_id = models.PositiveIntegerField(db_index=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    order = models.IntegerField(blank=True, null=True, db_index=True,
                                verbose_name=_('order'))

    objects = CategorizationManager()

    @property
    def object_modification_date(self):
        return self.content_object.modification_date

    @property
    def object_creation_date(self):
        return self.content_object.creation_date

    def __repr__(self):
        return '<%s@%s>' % (repr(self.content_object), repr(self.category))

    class Meta:
        verbose_name = _('categorization')
        verbose_name_plural = _('categorizations')
        ordering = ('order', '-id')


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
