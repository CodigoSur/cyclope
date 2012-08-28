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
from captcha.fields import CaptchaField
from models import CustomComment

class CustomCommentForm(ThreadedCommentForm):
    url = forms.URLField(label=_("Website or Blog"), required=False)
    captcha = CaptchaField(label=_("Security code"))
    subscribe = forms.BooleanField(help_text=_('I want to be notified by email ' \
                                               'when there is a new comment.'),
                                   required=False)

    def clean(self):
        # captcha_ input only exists when the user is authenticated
        if 'captcha_' in self.data:
            if 'captcha' in self._errors:
                self._errors.pop('captcha')
        return super(CustomCommentForm, self).clean()

    def get_comment_model(self):
        return CustomComment
