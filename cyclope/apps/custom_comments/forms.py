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
from django.utils.translation import ugettext_lazy as _

from threadedcomments.forms import ThreadedCommentForm
from captcha.fields import CaptchaField, CaptchaTextInput
from models import CustomComment


class CustomCaptchaTextInput(CaptchaTextInput):
    """
    This is the same as CaptchaTextInput but with 'deferred' image loading via
    javascript. The image html tag has a 'src_' attr instead of 'src'.
    """
    def render(self, name, value, attrs=None):
        ret = super(CustomCaptchaTextInput, self).render(name, value, attrs=None)
        return ret.replace("src=", "src_=")


class CustomCaptchaField(CaptchaField):

    def __init__(self, *args, **kwargs):
        super(CustomCaptchaField, self).__init__(*args, **kwargs)
        self.widget = CustomCaptchaTextInput(**{'output_format': u'%(image)s %(hidden_field)s %(text_field)s'})


class CustomCommentForm(ThreadedCommentForm):
    url = forms.URLField(label=_("Website or Blog"), required=False)
    captcha = CustomCaptchaField(label=_("Security code"))
    subscribe = forms.BooleanField(help_text=_('I want to be notified by email ' \
                                               'when there is a new comment.'),
                                   required=False)

    def clean(self):
        # captcha_ input only exists when the user is authenticated
        # this is not a real validation, submiting the form without the captcha_
        # will pass. The problem is that there's no way to know if the user us logged in
        # without rewriting a couple of views and template tags or use something like
        # django-contrib-requestprovider
        if 'captcha_' in self.data:
            if 'captcha' in self._errors:
                self._errors.pop('captcha')
        return super(CustomCommentForm, self).clean()

    def user_is_authenticated(self):
        del self.fields["captcha"]
        del self.fields["honeypot"]

    def get_comment_model(self):
        return CustomComment
