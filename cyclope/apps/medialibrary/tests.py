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


from cyclope.tests import ViewableTestCase
from models import *

class PictureTestCase(ViewableTestCase):
    test_model = Picture


class DocumentTestCase(ViewableTestCase):
    test_model = Document


class FlashMovieTestCase(ViewableTestCase):
    test_model = FlashMovie

    def setUp(self):
        super(FlashMovieTestCase, self).setUp()
        self.test_object = FlashMovie.objects.create(name='An instance', flash="/")


class MovieClipTestCase(ViewableTestCase):
    test_model = MovieClip


class SoundTrackTestCase(ViewableTestCase):
    test_model = SoundTrack


class RegularFileTestCase(ViewableTestCase):
    test_model = RegularFile


class ExternalContentTestCase(ViewableTestCase):
    test_model = ExternalContent
