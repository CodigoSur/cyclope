#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010-2012 Código Sur Asociación Civil
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


from django.contrib import admin
from django import forms

from cyclope.core.collections.admin import CollectibleAdmin
from cyclope.admin import BaseContentAdmin

from models import Topic

class TopicForm(forms.ModelForm):

    class Meta:
        model = Topic

class TopicAdmin(CollectibleAdmin, BaseContentAdmin):
    form = TopicForm

admin.site.register(Topic, TopicAdmin)
