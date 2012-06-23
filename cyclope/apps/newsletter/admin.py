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

from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy as _

from mptt.forms import TreeNodeChoiceField

from cyclope.apps.newsletter.models import Newsletter
from cyclope.core.collections.models import Category
from cyclope.models import SiteSettings
from cyclope.core.frontend.sites import site
from cyclope.utils import get_singleton

class NewsletterAdminForm(forms.ModelForm):
    content_category = TreeNodeChoiceField(
        queryset=Category.tree.all(), label=_('Current content category'),
        help_text=_('This is the category which groups the content that will be sent with the newsletter.'))
    view = forms.ChoiceField(label=_('View'))

    def __init__(self, *args, **kwargs):
        super(NewsletterAdminForm, self).__init__(*args, **kwargs)
        nl_collection = get_singleton(SiteSettings).newsletter_collection
        self.fields['content_category'].queryset = Category.tree.filter(collection=nl_collection)
        self.fields['content_category'].initial = Category.objects.latest()

        views = [('', '------')]
        views.extend([(view.name, view.verbose_name)
                       for view in site.get_views(Newsletter)
                       if view.is_content_view])
        self.fields['view'].choices = views

    class Meta:
        model = Newsletter


class NewsletterAdmin(admin.ModelAdmin):
    form = NewsletterAdminForm
    change_form_template = "admin/newsletter_change_form.html"

admin.site.register(Newsletter, NewsletterAdmin)
