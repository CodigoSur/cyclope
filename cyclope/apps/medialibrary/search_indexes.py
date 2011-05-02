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

from haystack.indexes import *
from haystack import site
import cyclope.apps.medialibrary.models


class BaseMediaIndex(RealTimeSearchIndex):
    text = CharField(document=True, use_template=True) #template: author, description
    author = CharField(model_attr='author', null=True)

class PictureIndex(BaseMediaIndex):
    pass
site.register(cyclope.apps.medialibrary.models.Picture, PictureIndex)

class SoundTrackIndex(BaseMediaIndex):
    pass
site.register(cyclope.apps.medialibrary.models.SoundTrack, SoundTrackIndex)

class MovieClipIndex(BaseMediaIndex):
    pass
site.register(cyclope.apps.medialibrary.models.MovieClip, MovieClipIndex)

class DocumentIndex(BaseMediaIndex):
    pass
site.register(cyclope.apps.medialibrary.models.Document, DocumentIndex)

class FlashMovieIndex(BaseMediaIndex):
    pass
site.register(cyclope.apps.medialibrary.models.FlashMovie, FlashMovieIndex)

class RegularFileIndex(BaseMediaIndex):
    pass
site.register(cyclope.apps.medialibrary.models.RegularFile, RegularFileIndex)

class ExternalContentIndex(BaseMediaIndex):
    pass
site.register(cyclope.apps.medialibrary.models.ExternalContent, ExternalContentIndex)
