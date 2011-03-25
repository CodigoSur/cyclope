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
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.utils.importlib import import_module

import cyclope.settings as cyc_settings
from cyclope.admin import BaseContentAdmin
from cyclope.core.collections.admin import CollectibleAdmin

from models import Contact, ContactAddress
from forms import ContactForm

class ContactAddressInline(admin.StackedInline):
    model = ContactAddress
    extra = 0
    fields = ('type', 'country', 'region', 'city', 'zip_code', 'street_address', 'phone_number',
              'post_office_box')

class ContactAdmin(CollectibleAdmin, BaseContentAdmin):
    form = ContactForm
    inlines = CollectibleAdmin.inlines + BaseContentAdmin.inlines + [ContactAddressInline]

    list_filter = CollectibleAdmin.list_filter + ('gender', )
    list_display = ('given_name', 'surname', 'gender', 'email', 'web', 'mobile_phone_number')
    search_fields = ('given_name', 'surname', 'email', 'web', 'mobile_phone_number')

    fieldsets = (
        (None, {
            'fields': ('given_name', 'surname', 'birth_date', 'photo', 'gender',
                       'email', 'web', 'mobile_phone_number')
        }),
    )

    # Add ContactProfile admin as inline if defined in settings
    if getattr(settings, 'CYCLOPE_CONTACTS_PROFILE_ADMIN_INLINE_MODULE', False):
        _parts = settings.CYCLOPE_CONTACTS_PROFILE_ADMIN_INLINE_MODULE.split('.')
        _inl = _parts[-1]
        _mod = ".".join(_parts[:-1])
        _module = import_module(_mod)
        profile_inline = getattr(_module, _inl)
        inlines.append(profile_inline)



admin.site.register(Contact, ContactAdmin)
