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

from django.db import models
from django.test import TestCase

from . import FrontendView, site


class FrontendTestCase(TestCase):

    class Model(models.Model):
        name = "Test"

    class ModelDetail(FrontendView):
        name = 'model-detail'
        verbose_name = 'show a model'
        is_default = True
        is_instance_view = True
        is_region_view = False
        is_content_view = True

    def setUp(self):
        site.register_view(self.Model, self.ModelDetail)

    def tearDown(self):
        site.unregister_view(self.Model, self.ModelDetail)

    def test_register_view(self):
        view = site.get_view(self.Model, 'model-detail')
        self.assertTrue(isinstance(view, self.ModelDetail))

    def test_get_view(self):
        view = site.get_view(self.Model, 'model-detail')
        self.assertTrue(isinstance(view, self.ModelDetail))

        # Test with instance
        view = site.get_view(self.Model(), 'model-detail')
        self.assertTrue(isinstance(view, self.ModelDetail))

    def test_get_views(self):
        views = site.get_views(self.Model())
        self.assertEqual(len(views), 1)
        self.assertTrue(all([isinstance(v, self.ModelDetail) for v in views]))

    def test_unregister(self):
        site.register_view(self.Model, self.ModelDetail)
        site.unregister_view(self.Model, self.ModelDetail)
        views = site.get_views(self.Model())
        self.assertEqual(len(views), 0)

    def test__name__expected(self):
        view = site.get_view(self.Model, 'model-detail')
        self.assertEqual(view.__name__, view.name)




