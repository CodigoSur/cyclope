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


"""
apps.contacts.models
--------------------
"""

from django.db import models
from django.utils.translation import ugettext_lazy as _

from cyclope.models import BaseContent
from cyclope.core.collections.models import Collectible


class Country(models.Model):
    name = models.CharField(_('name'), max_length=255)
    # iso ?

class Region(models.Model):
    country = models.ForeignKey(Country)
    name = models.CharField(_('name'), max_length=255)

class City(models.Model):
    region = models.ForeignKey(Region)
    name = models.CharField(_('name'), max_length=255)

class Location(models.Model):
    country = models.ForeignKey(Country, verbose_name=_('country'),blank=True, null=True)
    region = models.ForeignKey(Region, verbose_name=_('region'), blank=True, null=True)
    city = models.ForeignKey(City, verbose_name=_('city'), blank=True, null=True)
    street_address = models.CharField(_('street address'), blank=True, max_length=255)
    phone_number = models.CharField(max_length=40, verbose_name=_('phone number'), blank=True)
    post_office_box = models.CharField(_('postal box'), blank=True, max_length=255)

    class Meta:
        abstract = True

    def __unicode__(self):
        return "%s %s, %s, %s" % (self.street_address, self.city, self.region, self.country)


