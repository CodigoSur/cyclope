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
This app implements DynamicForms using django-forms-builder.
"""
from django.utils.translation import ugettext_lazy as _

from captcha.fields import CaptchaField

# Monkeypatching forms_builder.
# fields must me monkeypatched before of models!
from forms_builder.forms import fields as _fields

# Adding Captcha to field options
CAPTCHA = 101
_fields.CAPTCHA = CAPTCHA

_fields.NAMES = _fields.NAMES + ((CAPTCHA, _("Security code")),)

_fields.CLASSES[CAPTCHA] = CaptchaField

# now monkeypatching the model
from forms_builder.forms.models import Form as _Form

# Registered models must have a name attribute
_Form.name = property(lambda self:self.title)

_Form._meta.verbose_name = _('form')
_Form._meta.verbose_name_plural = _('forms')

DynamicForm = _Form
