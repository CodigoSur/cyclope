#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010-2012 Código Sur - Nuestra América Asoc. Civil / Fundación Pacificar.
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

# based on  shestera's django-multisite
# http://github.com/shestera/django-multisite

from threading import local

_thread_locals = local()

class DynamicSetting(object):
    def __init__(self, setting_name):
        # the name of the setting whose value we will hold in _thread_locals
        self.setting_name = setting_name

    def set(self, value):
        "Sets the value for this setting in _thread_locals"
        setattr(_thread_locals, self.setting_name, value)

    def __getitem__(self, attr):
        current = getattr(_thread_locals, self.setting_name, None)
        return current.__getitem__(attr)

    def __setitem__(self, attr, value):
        raise NotImplemented
        #current = getattr(_thread_locals, self.setting_name, None)
        #current.__setitem__(attr, value)

    def __getattribute__(self, attr):

        if attr == 'setting_name':
            return super(DynamicSetting, self).__getattribute__(attr)
        elif attr == '__setitem__':
            print "set item"
            return super(DynamicSetting, self).__getattribute__(attr)
        elif attr == '__getitem__':
            print "get item"
            return super(DynamicSetting, self).__getattribute__(attr)

        current = getattr(_thread_locals, self.setting_name, None)
        if hasattr(current, attr):
            return getattr(current, attr)
        else:
            return super(DynamicSetting, self).__getattribute__(attr)


class RequestHostHook(object):
    def __repr__(self):
        if not hasattr(_thread_locals, "REQUEST_HOST"):
            _thread_locals.REQUEST_HOST = ""
        return _thread_locals.REQUEST_HOST

    def set(self, value):
        _thread_locals.REQUEST_HOST = value

    def get(self):
        return _thread_locals.REQUEST_HOST

    def get_module_name(self):
        return repr(self)


class MediaRootHook(object):
    def __repr__(self):
        if not hasattr(_thread_locals, "MEDIA_ROOT"):
            _thread_locals.MEDIA_ROOT = ""
        return _thread_locals.MEDIA_ROOT

    def set(self, value):
        _thread_locals.MEDIA_ROOT = value

    def endswith(self, val):
        return str(self).endswith(val)

    def __add__(self, other):
        return str(self) + other


