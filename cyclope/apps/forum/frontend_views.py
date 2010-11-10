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
from django.core.exceptions import ObjectDoesNotExist

from cyclope.core import frontend
from cyclope import views

from models import Topic


class TopicDetail(frontend.FrontendView):
    name = 'detail'
    verbose_name=_('detailed view of the selected Topic')
    is_default = True
    is_instance_view = True
    is_content_view = True

    def get_response(self, request, host_template, content_object):

        try:
            profile = content_object.author.get_profile()
            avatar = profile.avatar
        except ObjectDoesNotExist:
            avatar = None

        context = {'avatar': avatar}
        return views.object_detail(request, host_template, content_object,
                                   extra_context=context)

frontend.site.register_view(Topic, TopicDetail)
