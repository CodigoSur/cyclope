#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2012 Código Sur Sociedad Civil.
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
GenericModelChoiceField based on django-autocomplete-light
from James Pic and contributors.
https://github.com/yourlabs/django-autocomplete-light
"""


from django import forms
from django.db import models
from django.forms import fields
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType

class GenericModelChoiceField(fields.Field):
    """
    Simple form field that converts strings to models.
    """
    def validate(self, value):
        super(GenericModelChoiceField, self).validate(value)
        if not value and not self.required:
            return True

        value = self.prepare_value(value)
        try:
            self.to_python(value)
        except:
            raise forms.ValidationError(_(u'field %(field)s cannot validate %(value)s') %
                                        {"field":self, "value":value})

    def prepare_value(self, value):
        """
        Given a model instance as value, with content type id of 3 and pk of 5,
        return such a string '3-5'.
        """
        if isinstance(value, (str, unicode)):
            # Apparently there's a bug in django, that causes a python value to
            # be passed here. This ONLY happens when in an inline ....
            return value
        elif isinstance(value, models.Model):
            return '%s-%s' % (ContentType.objects.get_for_model(value).pk,
                              value.pk)

    @classmethod
    def to_python(self, value):
        """
        Given a string like '3-5', return the model of content type id 3 and pk
        5.
        """
        if not value:
            return None
        try:
            content_type_id, object_id = value.split('-')
            content_type = ContentType.objects.get_for_id(content_type_id)
        except (ContentType.DoesNotExist, ValueError):
            raise forms.ValidationError(_(u'Wrong content type or object'))
        else:
            model = content_type.model_class()

        return model.objects.get(pk=object_id)
