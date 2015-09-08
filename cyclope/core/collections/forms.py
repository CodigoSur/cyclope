#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010 - 2015 Código Sur Sociedad Civil
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

from django.conf import settings
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from mptt.forms import TreeNodeChoiceField

from django.utils.translation import ugettext_lazy as _

from cyclope.core.collections.models import Category

class ContentFilterForm(forms.Form):
#    helper = FormHelper()
    def __init__(self, collections, *args, **kwargs):
        super(ContentFilterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'content-filter-form'
        self.helper.form_method = 'get'
        self.helper.add_input(Submit('submit', _('Filter')))
        self.helper.form_class = 'form-filter'
        print self.fields.items()
        for collection in collections:
            self.fields[collection.slug] = TreeNodeChoiceField(label=_(collection.name),
              queryset=Category.tree.filter(collection=collection), required=False)
