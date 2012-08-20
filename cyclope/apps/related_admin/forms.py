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
GenericModelForm  based on django-autocomplete-light
from James Pic and contributors.
https://github.com/yourlabs/django-autocomplete-light
"""

from django import forms
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey


class GenericModelForm(forms.ModelForm):
    """
    This simple subclass of ModelForm fixes a couple of issues with django's
    ModelForm.

    - treat virtual fields like GenericForeignKey as normal fields, Django
      should already do that but it doesn't,
    - when setting a GenericForeignKey value, also set the object id and
      content type id fields, again Django could probably afford to do that.
    """
    def __init__(self, *args, **kwargs):
        """
        What ModelForm does, but also add virtual field values to self.initial.
        """
        super(GenericModelForm, self).__init__(*args, **kwargs)

        # do what model_to_dict doesn't
        for field in self._meta.model._meta.virtual_fields:
            self.initial[field.name] = getattr(self.instance, field.name, None)

    def _post_clean(self):
        """
        What ModelForm does, but also set virtual field values from
        cleaned_data.
        """
        super(GenericModelForm, self)._post_clean()
        # take care of virtual fields since django doesn't
        for field in self._meta.model._meta.virtual_fields:
            value = self.cleaned_data.get(field.name, None)

            if value:
                setattr(self.instance, field.name, value)

    def save(self, commit=True):
        """
        What ModelForm does, but also set GFK.ct_field and GFK.fk_field if such
        a virtual field has a value.

        This should probably be done in the GFK field itself, but it's here for
        convenience until Django fixes that.
        """
        for field in self._meta.model._meta.virtual_fields:
            if isinstance(field, GenericForeignKey):
                value = self.cleaned_data.get(field.name, None)

                if not value:
                    continue

                setattr(self.instance, field.ct_field,
                        ContentType.objects.get_for_model(value))
                setattr(self.instance, field.fk_field, value.pk)

        return super(GenericModelForm, self).save(commit)

    def clean(self):
        super(GenericModelForm, self).clean()
        # Add fk_fields of GenericFK to cleaned data (for inline forms)
        for field in self._meta.model._meta.virtual_fields:
            if isinstance(field, GenericForeignKey):
                value = self.cleaned_data.get(field.name, None)

                if not value:
                    continue
                self.cleaned_data[field.fk_field] = value.pk
        return self.cleaned_data

