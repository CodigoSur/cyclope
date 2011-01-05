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
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.models import User, SiteProfileNotAvailable

from cyclope.models import BaseContent
from cyclope.core.collections.models import Collectible

from cyclope.apps.locations.models import Location
from autoslug.fields import AutoSlugField

ADDRESS_TYPE_CHOICES = (
    ('work', _('work')),
    ('home', _('home')),
)

class ContactAddress(Location):
    type = models.CharField(max_length=1, choices=ADDRESS_TYPE_CHOICES)
    contact = models.ForeignKey("Contact")

class Contact(BaseContent, Collectible):
    given_name = models.CharField(_('given name'), max_length=255)
    family_name = models.CharField(_('family name'), blank=True, max_length=255)
    gender = models.CharField(max_length=1, choices=(('M', _('Male')), ('F', _('Female'))))
    email = models.EmailField(blank=True)
    web = models.CharField(max_length=255, blank=True)
    mobile_phone_number = models.CharField(max_length=40, blank=True)

    class Meta:
        verbose_name = _('contact')
        verbose_name_plural = _('contacts')

    def __unicode__(self):
        if self.family_name:
            return u"%s %s" % (self.given_name, self.family_name)
        else:
            return self.given_name

    def save(self, *args, **kwargs):
        self.name = unicode(self)
        super(BaseContent, self).save(*args, **kwargs)
        super(Collectible, self).save(*args, **kwargs)

    def get_profile(self):
        """
        Returns site-specific profile for this contact. Raises
        SiteProfileNotAvailable if this site does not allow profiles.
        """
        if not hasattr(self, '_profile_cache'):
            from django.conf import settings
            if not getattr(settings, 'CYCLOPE_CONTACTS_PROFILE_MODULE', False):
                raise SiteProfileNotAvailable('You need to set CYCLOPE_CONTACTS'
                                              '_PROFILE_MODULE in your project settings')
            try:
                app_label, model_name = settings.CYCLOPE_CONTACTS_PROFILE_MODULE.split('.')
            except ValueError:
                raise SiteProfileNotAvailable('app_label and model_name should'
                        ' be separated by a dot in the CYCLOPE_CONTACTS_PROFILE'
                        '_MODULE setting')

            try:
                model = models.get_model(app_label, model_name)
                if model is None:
                    raise SiteProfileNotAvailable('Unable to load the profile '
                        'model, check CYCLOPE_CONTACTS_PROFILE_MODULE in your '
                        'project settings')
                self._profile_cache = model._default_manager.using(self._state.db).get(contact__id__exact=self.id)
                self._profile_cache.user = self
            except (ImportError, ImproperlyConfigured):
                raise SiteProfileNotAvailable
        return self._profile_cache

    def has_profile(self):
        """
        Returns True if contacts are extended with a profile.
        """
        from django.conf import settings
        if not getattr(settings, 'CYCLOPE_CONTACTS_PROFILE_MODULE', False):
            return False
        return True

