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

import inspect
from threading import local

_thread_locals = local()

_dont_override = set(['__repr__', '__getattribute__', '__new__',
                      '__init__', '__setitem__'])

class _None(object):
    pass

class DynamicSetting(object):
    def __init__(self, setting_name, value_or_type):
        value, type_ = _None, None
        if isinstance(value_or_type, type):
            type_ = value_or_type
        else:
            type_ = type(value_or_type)
            value = value_or_type

        self.__class__ = type('DS%s' % repr(type_), (self.__class__, object), {})

        self.setting_name = setting_name
        if value is not _None:
            self.set(value)

        methods = set()
        for name, attr in type_.__dict__.iteritems():
            if inspect.ismethod(attr) or inspect.ismethoddescriptor(attr):
                methods.add(name)
        methods_to_override = methods - _dont_override

        def method(self, *args, **kwargs):
            return getattr(self.get_value(), name)

        for name in methods_to_override:
            def method(self, *args, **kwargs):
                print name, args, kwargs
                return type_.__dict__[name](*args, **kwargs)

            def outer(name, *args, **kwargs):
                def inner(self, *args, **kwargs):
                    return getattr(self.get_value(), name)(*args, **kwargs)
                return inner
            setattr(self.__class__, name, outer(name))

    def set(self, value):
        "Sets the value for this setting in _thread_locals"
        if isinstance(value, tuple):
            tuple_format = "%s__tuple-%s"
            value = tuple([DynamicSetting(tuple_format % (self.setting_name, n), element)
                           for n, element in enumerate(value)])
        if isinstance(value, dict):
            dic = {}
            for key, val in value.iteritems():
                dict_format = "%s__dict-%s"
                dic[key] = DynamicSetting(dict_format % (self.setting_name, key), val)
            value = dic
        setattr(_thread_locals, self.setting_name, value)

    def get_value(self):
        "Gets the settings actual value"
        return getattr(_thread_locals, self.setting_name, None)

    def __nonzero__(self):
        return bool(self.get_value())

    def __setitem__(self, attr, value):
        raise NotImplementedError

    def __repr__(self):
        val = self.get_value()
        return "<DynamicSetting: %s>" % repr(val)

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


