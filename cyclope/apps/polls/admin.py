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
from django.utils.translation import ugettext_lazy as _
import cyclope.settings as cyc_settings

from models import *

class AnswerInline(admin.StackedInline):
    model = Answer

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
    list_filter = ('poll',)
    fields = ('text', 'allow_multiple_answers',)

    def changelist_view(self, request, extra_context=None):
        # questions changelist should only show items from one poll.
        # so we activate the filter to display the last poll questions when no
        # filters have been selected by the user
        if Poll.objects.count():
            last_poll_id = Poll.objects.order_by('-pk')[0].id
            if not request.GET:
                request.GET = {u'poll__id__exact': unicode(last_poll_id)}
        return super(QuestionAdmin, self).changelist_view(request, extra_context)

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 0

class PollAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]

    class Media:
        # This js is needed because drag&drop will be used
        js = (
            cyc_settings.CYCLOPE_STATIC_URL + 'js/reuse_django_jquery.js',
            cyc_settings.CYCLOPE_STATIC_URL + 'js/jquery-ui-1.8.4.custom.min.js',
        )

admin.site.register(Question, QuestionAdmin)
admin.site.register(Poll, PollAdmin)
