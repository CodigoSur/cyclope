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

from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from models import UserProfile

class UserProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        # Add User's fields first in the form
        self.fields.keyOrder =  ['first_name', 'last_name', 'email'] + self.fields.keyOrder[:-3]
        try:
            self.fields['email'].initial = self.instance.user.email
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
        except User.DoesNotExist:
            pass

    first_name = forms.CharField(label=_('first name'), max_length=30, required=False)
    last_name = forms.CharField(label=_('last name'), max_length=30, required=False)
    email = forms.EmailField()

    class Meta:
        model = UserProfile
        exclude = ('user',)

    def save(self, *args, **kwargs):
        user = self.instance.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        # change the email only if nobody is using it
        user_same_email = User.objects.filter(email=self.cleaned_data['email'])
        if user == user_same_email:
            user.email = self.cleaned_data['email']
        user.save()
        profile = super(UserProfileForm, self).save(*args,**kwargs)
        return profile
