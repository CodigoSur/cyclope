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
This app implements DynamicForms using django-forms-builder
"""

from django.utils.translation import ugettext_lazy as _

from models import DynamicForm
from forms_builder.forms.views import form_detail

from cyclope.core import frontend
from cyclope import views

class FormDetail(frontend.FrontendView):
    """Display a DynamicForm
    """
    name='form-detail'
    verbose_name=_('show a form')
    is_default = True
    is_instance_view = True
    is_region_view = False
    is_content_view = True

    def get_response(self, request, req_context, options, content_object):
        return form_detail(request, content_object.slug)

frontend.site.register_view(DynamicForm, FormDetail)
