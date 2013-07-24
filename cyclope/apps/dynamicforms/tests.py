#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010-2013 Código Sur Sociedad Civil
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

from django.contrib.sites.models import Site

from cyclope.tests import ViewableTestCase

from models import DynamicForm

class DynamicFormTestCase(ViewableTestCase):
    test_model = DynamicForm

    def setUp(self):
        super(DynamicFormTestCase, self).setUp()
        form = DynamicForm.objects.create(title="An instance")
        form.sites.add(Site.objects.get_current())
        form.save()
        form.fields.create(label="field", field_type=1, required=True, visible=True)
        self.test_object = form

    def test_empty_form(self):
        url = u'/form/%s/' % self.test_object.slug
        response = self.client.post(url, data={})
        self.assertEqual(response.status_code, 200)
