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

from django.contrib.auth.models import User

from cyclope.tests import ViewableTestCase

from models import Topic

class TopicTestCase(ViewableTestCase):
    test_model = Topic

    def setUp(self):
        super(TopicTestCase, self).setUp()
        self.user = User.objects.create_user('john', 'le@non.com', 'lennon')
        self.test_object = Topic(name='An instance', user=self.user)
        self.test_object.save()

