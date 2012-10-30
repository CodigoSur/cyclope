#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright 2012 Código Sur Sociedad Civil.
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

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from autoslug.fields import AutoSlugField
from registration import signals as registration_signals

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    slug = AutoSlugField(populate_from=lambda obj:obj.user.username, unique=True,
                         null=False, db_index=True)
    avatar = models.ImageField(_('avatar'), max_length=100,
                               blank=True, upload_to="uploads/avatars/")
    city = models.CharField(_('city'), max_length=100, blank=True)
    about = models.TextField(_('about myself'), max_length=1000, blank=True)

    public = models.BooleanField(
        _('public'), default=True,
        help_text=_('Choose whether your profile info should be publicly visible or not'))

    @models.permalink
    def get_absolute_url(self):
        return ('userprofile-detail', (), { 'slug': self.slug })

    def __unicode__(self):
        return self.user.get_full_name() or self.user.username

    def save(self, *args, **kwargs):
        super(UserProfile, self).save(*args, **kwargs)
        # This is a hack to deal with profiles that aren't created automatically by a signal
        # so the user is not part of the profile instance in the save method
        # Instead, the form save is issued from the profile model
        form = getattr(self, "_form", None)
        if form:
            form.instance = self
            form.save()

User.get_absolute_url = lambda self: self.get_profile().get_absolute_url()

# Signal callbacks

def _create_profile_upon_activation(*args, **kwargs):
    UserProfile.objects.create(user=kwargs['user'])

registration_signals.user_activated.connect(_create_profile_upon_activation)
