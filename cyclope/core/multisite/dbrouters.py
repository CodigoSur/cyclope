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

from django.conf import settings

from threading import local

_thread_locals = local()

class MultiSiteRouter(object):
    """A router to control all database operations on models"""

    def db_for_read(self, model, **hints):
        "choose the db according to the current host from request"
        connection = settings.REQUEST_HOST.get_module_name()
        return connection

    def db_for_write(self, model, **hints):
        "choose the db according to the current host from request"
        connection = settings.REQUEST_HOST.get_module_name()
        return connection

    def allow_relation(self, obj1, obj2, **hints):
        #if 'multisite' in [obj1._meta.app_label, obj2._meta.app_label]:
        #    return False

        return True

    def allow_syncdb(self, db, model):
        #if model._meta.app_label == 'multisite':
        # return True
        return True

