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
Based on patches #9976 (https://code.djangoproject.com/ticket/9976)

"""

import re

from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.template.loader import render_to_string
from django.contrib.admin.widgets import ForeignKeyRawIdWidget

from views import do_render_object
from fields import GenericModelChoiceField
from cyclope.utils import get_app_label, get_object_name


class GenericFKWidget(ForeignKeyRawIdWidget):
    def __init__(self, ct_field, cts=None, attrs=None, template="related_admin/gfk_widget.html"):
        self.ct_field = ct_field
        if cts is None:
            cts = []
        self.cts = cts
        self.template = template
        forms.TextInput.__init__(self, attrs)

    def render(self, name, value, attrs=None):
        # if it is inline build the proper ct_field name
        ct_field = self.ct_field

        if "__prefix__" in name:
            ct_field = re.sub('__prefix__.*', "__prefix__-" + ct_field, name)
        elif re.match('.*\-(\d+\-).*', name):
            ct_field = re.sub('(\d+\-).*', "\g<1>" + ct_field , name)
        self._test_ct_field = ct_field # for testing purposes only
        actual_object = self.get_actual_object(value)
        if attrs is None:
            attrs = {}
        params = self.url_parameters()
        d = {
            'url': ('?' + '&amp;'.join(['%s=%s' % (k, v) for k, v in params.iteritems()])) if params else "",
            'obj_repr': do_render_object(actual_object) if actual_object else "",
            'value': value,
            'name': name,
            'ct_field': ct_field,
            'static_admin': settings.STATIC_URL + "admin/",
            'content_types': [(ContentType.objects.get_for_model(ct).pk,
                              get_app_label(ct), get_object_name(ct)) \
                              for ct in self.cts],
        }
        return render_to_string(self.template, d)

    def get_actual_object(self, value):
        try:
            actual_object = GenericModelChoiceField.to_python(value)
        except forms.ValidationError:
            actual_object = None
        return actual_object

    def url_parameters(self):
        return {}
