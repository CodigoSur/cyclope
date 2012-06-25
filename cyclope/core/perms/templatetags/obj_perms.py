#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2012 Código Sur Asoc. Civil
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
core.perms.templatetags
-----------------------
"""

from django import template
from django.contrib.auth import load_backend 

register = template.Library()


class CategoryPerms(template.Node):
    """Returns a dictionary containing the categoty based permissions the current user has for the current object.
    
    Syntax::
        {% category_perms [object] as [var_name] %}
    Example::
        {% category_perms current_object as cat_perms %}
    """
    def __init__(self, obj_var, var_name):
        self.var_name = var_name
        self.obj_var = obj_var

    def render(self, context):
        obj = context[self.obj_var]
        user = context["user"]
        cat_perm_backend = load_backend('cyclope.core.perms.backends.CategoryPermBackend')
        context[self.var_name] = cat_perm_backend.get_all_permissions(user, obj)
        return ''

@register.tag('per_category_perms')
def do_category_perms(parser, token):
    bits = token.contents.split()
    if bits[-2] != 'as':
        raise template.TemplateSyntaxError, "Missing 'as' argument for '%s' tag" % bits[0]
    return CategoryPerms(bits[1], bits[-1])
