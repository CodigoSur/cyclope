#!/usr/bin/env python
# -*- coding: UTF-8 -*-
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


"""
apps.polls.models
--------------------
"""

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from cyclope.models import BaseContent
from cyclope.core.collections.models import Collectible

class Poll(BaseContent, Collectible):
    description = models.TextField(_('description'), blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('poll')
        verbose_name_plural = _('polls')


class Question(models.Model):
    poll = models.ForeignKey(Poll, editable=False)
    text = models.CharField(_('text'), blank=False,
                            db_index=True, max_length=255)
    order = models.IntegerField(null=True, blank=True)
    allow_multiple_answers = models.BooleanField(
        _('allow multiple answers'), default=False)
    #allow_unlisted = models.BooleanField(
    #    _('allow unlisted answer'), default=True)

    def __unicode__(self):
        return self.text

    class Meta:
        verbose_name = _('question')
        verbose_name_plural = _('questions')
        ordering = ('order',)


class Answer(models.Model):
    question = models.ForeignKey(Question, verbose_name=_('question'))
    text = models.CharField(_('text'), blank=False,
                            db_index=True, max_length=255)
    def get_votes(self):
        return Submission.objects.filter(answers=self).count()
    #unlisted = models.BooleanField(default=False, editable=False, db_index=True)

    def __unicode__(self):
        return self.text

    class Meta:
        verbose_name = _('answer')
        verbose_name_plural = _('answers')


class Submission(models.Model):
    poll = models.ForeignKey(Poll)
    user = models.ForeignKey(User, verbose_name=_('user'), null=True)
    foreign_user = models.CharField(_('foreign_user'), blank=True,
                                    db_index=True, max_length=60)
    answers = models.ManyToManyField(Answer, verbose_name=_('answers'))

    class Meta:
        verbose_name = _('submission')
        verbose_name_plural = _('submissions')
        ordering = ('poll', 'user')
