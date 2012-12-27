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

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, ButtonHolder

from models import UserProfile

class UserProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', _('Submit')))
        self.helper.layout = Layout(
            Fieldset(
                _('Personal information'),
                'first_name',
                'last_name',
                'email',
                'image',
                'description',
            )
        )
        super(UserProfileForm, self).__init__(*args, **kwargs)
        # Add User's fields first in the form
        self.fields.keyOrder =  ['first_name', 'last_name', 'email'] + self.fields.keyOrder[:-3]
        try:
            self.fields['email'].initial = self.instance.user.email
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
        except User.DoesNotExist:
            del self.fields['email']

    first_name = forms.CharField(label=_('First name'), max_length=30, required=False)
    last_name = forms.CharField(label=_('Last name'), max_length=30, required=False)
    email = forms.EmailField()

    class Meta:
        model = UserProfile
        exclude = ('user',)

    def save(self, *args, **kwargs):
        user = self.instance.user if self.instance.user_id else None
        if user:
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            # change the email only if nobody is using it
            email = self.cleaned_data.get('email')
            if email:
                user_same_email = User.objects.filter(email=email)
                if not user_same_email:
                    email = self.cleaned_data['email']
                elif user == user_same_email:
                    email = self.cleaned_data['email']
                else:
                    email = user.email
                user.email = email
            user.save()
            self.instance._form = None

        profile = super(UserProfileForm, self).save(*args, **kwargs)
        # This is a hack to deal with profiles that aren't created automatically by a signal
        # so the user is not part of the profile instance in the save method
        # Instead, the form save will be issued from the profile model
        profile._form = getattr(self.instance, "_form", self)
        return profile
