#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2013 Código Sur Sociedad Civil
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
from actstream import action
from actstream.models import Action

from cyclope.tests import ViewableTestCase

from models import Social


class SocialTestCase(ViewableTestCase):
    test_model = Social

    def setUp(self):
        user, created = User.objects.get_or_create(username="Foo")
        action.send(user,  verb='reached level 10', target=user)
        action.send(user,  verb='reached level 11', target=user)
        action.send(user,  verb='reached level 12')

