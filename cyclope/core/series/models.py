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

from django.db import models
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType

from cyclope.models import BaseContent
from cyclope.core.collections.models import Collectible


class SeriesContent(models.Model):

    self_type = models.ForeignKey(ContentType, verbose_name=_('content type'),
                                  related_name='series_contents_lt')
    self_id = models.PositiveIntegerField(db_index=True)

    other_type = models.ForeignKey(ContentType, verbose_name=_('content type'),
                                     related_name='series_contents_rt')
    other_id = models.PositiveIntegerField(db_index=True)

    self_object = generic.GenericForeignKey(ct_field='self_type',
                                                  fk_field='self_id')
    other_object = generic.GenericForeignKey(ct_field='other_type',
                                                  fk_field='other_id')

    order = models.IntegerField(blank=True, null=True, db_index=True)

    def __unicode__(self):
        return self.other_object.name

    class Meta:
        verbose_name = _('series content')
        verbose_name_plural = _('series contents')
        ordering = ['order', ]


class Series(BaseContent, Collectible):
    """Base model for Series contents.

    """
    description = models.TextField(_('description'), blank=True)

    image = models.ImageField(_('image'), max_length=100,
                               blank=True, upload_to="uploads/series/")

    series_contents = generic.GenericRelation(SeriesContent,
                                              object_id_field='self_id',
                                              content_type_field='self_type')

    # models allowed as series content
    content_models = []
    _cache_content_types = None

    @classmethod
    def get_content_types(cls):
        if cls._cache_content_types is None:
            dic = ContentType.objects.get_for_models(*cls.content_models)
            cls._cache_content_types = dic.values()
        return cls._cache_content_types

    @classmethod
    def get_content_models(cls):
        return cls.content_models

    @classmethod
    def get_content_types_choices(cls):

        dic = ContentType.objects.get_for_models(*cls.content_models)
        ctype_choices = map(lambda item: (item[1].id, item[0]._meta.verbose_name),
                            dic.iteritems())
        ctype_choices.insert(0, ('', '------'))
        return sorted(ctype_choices, key=lambda choice: choice[1])

    def get_content_objects(self):
        return [sc.other_object for sc in self.series_contents.all()]

    class Meta:
        verbose_name = _('series')
        verbose_name_plural = _('series')
        ordering = ['-creation_date', ]
        abstract = True
