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

from django.utils.translation import ugettext_lazy as _

from cyclope.core import frontend
from cyclope import views

from models import *

class MediaDetail(frontend.FrontendView):
    name='detail'
    is_default = True
    is_instance_view = True
    is_content_view = True
    params = {'template_object_name': 'media'}

    def get_response(self, request, req_context, options, content_object):
        return views.object_detail(request, req_context, content_object, **self.params)

class PictureDetail(MediaDetail):
    """Detail view of a Picture.
    """
    verbose_name=_('detailed view of the selected Picture')

frontend.site.register_view(Picture, PictureDetail)


class SoundTrackDetail(MediaDetail):
    """Detail view of an SoundTrack.
    """
    verbose_name=_('detailed view of the selected Audio Track')

frontend.site.register_view(SoundTrack, SoundTrackDetail)


class MovieClipDetail(MediaDetail):
    """Detail view of a MovieClip.
    """
    verbose_name=_('detailed view of the selected Movie Clip')

frontend.site.register_view(MovieClip, MovieClipDetail)


class DocumentDetail(MediaDetail):
    """Detail view of a Document.
    """
    verbose_name=_('detailed view of the selected Document')

frontend.site.register_view(Document, DocumentDetail)


class RegularFileDetail(MediaDetail):
    """Detail view of a regular file.
    """
    verbose_name=_('detailed view of the selected File')

frontend.site.register_view(RegularFile, RegularFileDetail)


class ExternalContentDetail(MediaDetail):
    """Detail view of external content.
    """
    verbose_name=_('detailed view of the selected External Content')

frontend.site.register_view(ExternalContent, ExternalContentDetail)


class FlashMovieDetail(MediaDetail):
    """Detail view of a Flash Movie.
    """
    verbose_name=_('detailed view of the selected Flash Movie')

    def get_response(self, request, req_context, options, content_object):
        p = content_object.flash.url_full
        i = p.rfind("/")+1
        base = p[:i]
        req_context.update({'url_base': base})
        return views.object_detail(request, req_context, content_object,
                                   **self.params)

frontend.site.register_view(FlashMovie, FlashMovieDetail)
