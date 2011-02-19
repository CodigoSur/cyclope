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
fields
------
"""

from django import forms
from django.core.exceptions import ValidationError

from cyclope.widgets import MultipleWidget

class MultipleField(forms.Field):
    def __init__(self, form=None, *args, **kwargs):
        """
        Field containing multiple fields that are gathered from a form that could
        be a forms.Form instance, a forms.Form class or None.
        """
        super(MultipleField, self).__init__(*args, **kwargs)
        if form is None:
            self.fields = {}
        else:
            if not hasattr(form, "fields"):
                form = form()
            self.fields = form.fields

        self.widget = MultipleWidget(self.fields)
        kwargs.setdefault('help_text', "")
        initial_data = self.fields.copy()
        for field in self.fields:
            initial_data[field] = initial_data[field].initial
        self.initial = initial_data


    def to_python(self, value):
        if value is None:
            return
        fields = self.fields.copy()
        errors = []
        for value_name in value:
            try:
                fields[value_name] = fields[value_name].clean(value[value_name])
            except ValidationError, e:
                if hasattr(e, 'code') and e.code in self.error_messages:
                    message = self.error_messages[e.code]
                    if e.params:
                        message = message % e.params
                    errors.append(message)
                else:
                    errors.extend(e.messages)
        if errors:
            raise ValidationError(errors)
        return fields

    def clean(self, value, validate=False):
        """
        Validates the given value and returns its "cleaned" value as an
        appropriate Python object.

        Raises ValidationError for any errors.
        """
        if not validate:
            value = {}
        else:
            value = self.to_python(value)
            self.validate(value)
            self.run_validators(value)
        return value
