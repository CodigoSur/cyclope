#!/usr/bin/env python
# -*- coding: UTF-8 -*-
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

from django.utils.translation import ugettext as _
from django.views.generic.list_detail import object_detail, object_list

from cyclope.core import frontend
from cyclope import views

from models import Shoe

class ShoeDetailView(frontend.FrontendView):
    """Detail view for Shoes"""
    name='detail'
    verbose_name=_('full detail')
    is_default = True
    params = {'queryset': Shoe.objects,
              'template_object_name': 'shoe',
             }

    def get_http_response(self, request, *args, **kwargs):
        return views.object_detail(request, inline=False, *args, **kwargs)

frontend.site.register_view(Shoe, ShoeDetailView())


class ShoeList(frontend.FrontendView):
    """Simple list view for Shoes.
    """
    name='list'
    verbose_name=_('list of Shoes')
    is_instance_view = False

    def get_http_response(self, request, *args, **kwargs):
        return views.object_list(request,
                           queryset=Shoe.objects.all(),
                           template_object_name= 'shoe',
                           *args, **kwargs)

    def get_string_response(self, request, *args, **kwargs):
        return views.object_list(request, inline=True,
                           queryset=Shoe.objects.all(),
                           template_object_name= 'shoe',
                           *args, **kwargs)

frontend.site.register_view(Shoe, ShoeList())
