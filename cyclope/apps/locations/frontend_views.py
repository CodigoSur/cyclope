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

from models import Location


#class LocationDetail(frontend.FrontendView):
    #"""Detail view for Locations"""
    #name='detail'
    #verbose_name=_('detailed view of the selected Location')
    #is_default = True
    #is_instance_view = True
    #is_content_view = True

    #def get_response(self, request, req_context, content_object):
        #context = {'content_relations': content_object.related_contents.all()}
        #return views.object_detail(request, req_context, content_object,
                                   #extra_context=context)

#frontend.site.register_view(Location, LocationDetail)


#class LocationTeaserList(frontend.FrontendView):
    #"""Teaser list view for Locations.
    #"""
    #name='teaser_list'
    #verbose_name=_('list of Location teasers')
    #is_instance_view = False
    #is_content_view = True
    #is_region_view = True

    #def get_response(self, request, req_context):
        #return views.object_list(request, req_context,
                                 #Location.objects.all(), view_name=self.name)


#frontend.site.register_view(Location, LocationTeaserList)
