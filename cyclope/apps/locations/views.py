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

from django.utils import simplejson as json

from django.http import HttpResponse

from models import Region, Country, City

def _make_choices(query_set):
    choices = [{'object_id': '', 'verbose_name': '------'}]
    choices.extend([{'object_id': model.id, 'verbose_name': unicode(model)}
                           for model in query_set])
    return choices

def regions_list(request):
    country_id = int(request.GET['q'])
    query_set = Region.objects.filter(country__id = country_id)
    json_data = json.dumps(_make_choices(query_set))
    return HttpResponse(json_data, mimetype = 'application/javascript')

def cities_list(request):
    region_id = int(request.GET['q'])
    query_set = City.objects.filter(region__id = region_id)
    json_data = json.dumps(_make_choices(query_set))
    return HttpResponse(json_data, mimetype = 'application/javascript')
