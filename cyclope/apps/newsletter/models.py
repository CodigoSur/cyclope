#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010-2013 Código Sur Sociedad Civil.
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
from cyclope.core.collections.models import Category, Categorization


class Newsletter(models.Model):
    name = models.CharField(_('name'), max_length=250,
                             unique=True, blank=False)
    slug = AutoSlugField(populate_from='name',
                         db_index=True, always_update=True)
    last_sent_date = models.DateTimeField(_('sent date'), editable=False, 
                                          null=True, blank=True)
    content_category = models.ForeignKey(Category)
    view = models.CharField(_('view'), max_length=255, default='default')
    regions = models.CharField(_('regions'), max_length=4,
        choices = (
            ('c', _('only central')),
            ('tc', _('top and central')),
            ('cl', _('central and lateral')),
            ('tcl', _('top, central and lateral')),
        ), default='c')
    n_contents_top = models.IntegerField(verbose_name=_('top'), default=0,
        help_text=_('Number of categorized contents to show in the top region.'))
    n_contents_center = models.IntegerField(verbose_name=_('center'), default=10, 
        help_text=_('Number of categorized contents to show in the central region.'))
    n_contents_lateral = models.IntegerField(verbose_name=_('lateral'), default=0,
        help_text=_('Number of categorized contents to show in the lateral region.'))
    head_image = models.ImageField(_('header newsletter'),
       upload_to='theme/images', blank=True, null=True,
       help_text=_('select image for head: 720px width x 124px height'))
    show_title = models.BooleanField(verbose_name=_("show title name in header"), 
        default=True)
    show_ToC = models.BooleanField(verbose_name=_("show table of contents"), 
        default=False)
    header = models.TextField(verbose_name=_('header'), blank=True,
        help_text=_('Text that will always be added on top of the content.'))
    layout = models.ForeignKey(Layout, verbose_name=_('layout'), 
        help_text=_('Layout to use to build the resulting HTML.'))
    sender_name = models.CharField(verbose_name=_('sender name'), 
        help_text=_('name that will displayed as the sender of the newsletter.'), 
        max_length=40, default="", blank=True)
    sender = models.EmailField(verbose_name=_('sender e-mail'), 
        help_text=_('e-mail address that will be used to send the newsletter.'))
    test_recipients = models.CharField(verbose_name=_('test recipients'), 
        help_text=_('comma separated list of test e-mail addresses'), 
        max_length=255)
    recipients = models.CharField(verbose_name=_('recipients'), 
        help_text=_('comma separated list of recipient e-mail addresses'), 
        max_length=255)
    list_admin = models.CharField(verbose_name=_('url list manager'), 
        help_text=_('creates a shortcut to the administrator of your mailing list (full url with http://)'), 
        max_length=255, blank=True)

    def __unicode__(self):
        return self.name

    def catz_by_region(self):
        data = Categorization.objects.get_for_category(self.content_category, 
                                        'modification_date', reverse=True)
        t, c, l = self.n_contents_top, self.n_contents_center, self.n_contents_lateral
        top, center, lateral = [], [], []
        if self.regions == "c":
            top, center, lateral = [], data[:c], []
        elif self.regions == "tc":
            top, center, lateral = data[:t], data[c:c+t], []
        elif self.regions == "cl":
            top, center, lateral = [], data[:c], data[c:c+l]
        elif self.regions == "tcl":
            top, center, lateral = data[:t], data[t:c+t], data[c+t:c+t+l]
        return top, center, lateral

    class Meta:
        verbose_name = _('newsletter')
        verbose_name_plural = _('newsletters')
