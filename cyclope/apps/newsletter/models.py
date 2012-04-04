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

from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

from autoslug.fields import AutoSlugField

from cyclope.utils import slugify
from cyclope.models import Layout
from cyclope.core.collections.models import Category

class Newsletter(models.Model):
    name = models.CharField(_('name'), max_length=250,
                             unique=True, blank=False)
    slug = AutoSlugField(populate_from='name',
                         db_index=True, always_update=True)
    last_sent_date = models.DateTimeField(_('sent date'),
                                          editable=False, null=True, blank=True)
    content_category = models.ForeignKey(Category)
    view = models.CharField(_('view'), max_length=255, default='default')
    show_ToC = models.BooleanField(verbose_name=_("show table of contents"), default=False)
    header = models.TextField(verbose_name=_('header'), help_text="Text that will always be added on top of the content.", blank=True)
    layout = models.ForeignKey(Layout, verbose_name=_('layout'), help_text="Layout to use to build the resulting HTML.")
    sender_name = models.CharField(verbose_name=_('sender name'), help_text="name that will displayed as the sender of the newsletter.",  max_length=40, default="", blank=True)
    sender = models.EmailField(verbose_name=_('sender e-mail'), help_text="e-mail address that will be used to send the newsletter.")
    test_recipients = models.CharField(verbose_name=_('test recipients'), help_text="comma separated list of test e-mail addresses", max_length=255)
    recipients = models.TextField(verbose_name=_('recipients'), help_text="comma separated list of recipient e-mail addresses")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('newsletter')
        verbose_name_plural = _('newsletters')
