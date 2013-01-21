#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2012 Código Sur Asociación Civil
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
core.perms.backends
-------------------
Authorizacion backends.
"""

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

from cyclope.core.collections.models import Categorization, Collectible, Category
from models import CategoryPermission


class CategoryPermBackend(object):
    supports_object_permissions = True
    supports_anonymous_user = False
    supports_inactive_user = False

    def authenticate(self, username, password):
        return None

    def _get_all_permissions(self, user_obj, obj=None):
        """Returns a queryset of all CategoryPermissions a user has over a Category or Collectible"""
        if obj is None or not user_obj.is_authenticated() or not user_obj.is_active:
            return CategoryPermission.objects.none()
        if issubclass(obj.__class__, Collectible):
            categorizations = Categorization.objects.get_for_object(obj)
            categories = [ c.category for c in categorizations ]
        elif issubclass(obj.__class__, Category):
            categories = [obj]
        return CategoryPermission.objects.filter(category__in=categories, user=user_obj)

    def get_all_permissions(self, user_obj, obj=None):
        """Returns a dictionary of permissions a user has over a Category or Collectible"""
        permissions = self._get_all_permissions(user_obj, obj)
        perms_dict = {}
        if permissions:
            for perm in ['edit_content', 'add_content']:
                perms_dict[perm] = permissions.filter(**{'can_%s' % perm: True}).exists()
        if user_obj.is_authenticated() and (user_obj.is_superuser or
           user_obj.is_staff and user_obj.has_perm('collections.change_category')):
            perms_dict["edit_content"] = True
            perms_dict["add_content"] = True
        return perms_dict

    def has_perm(self, user_obj, perm, obj=None):
        if obj is None:
            return False

        permissions = self._get_all_permissions(user_obj, obj)
        return permissions.filter(**{'can_%s' % perm: True}).exists()
