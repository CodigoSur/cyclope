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


from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect
from django.template import loader

from cyclope.core import frontend
from cyclope import views

from models import Poll, Submission, Question
from forms import QuestionForm, CaptchaForm

class PollSubmission(frontend.FrontendView):
    """Show or process a Poll Submission form"""

    name = 'submission'
    verbose_name=_('Poll submission form')
    is_content_view = True
    is_region_view = True

    def get_response(self, request, req_context, options, content_object):
        forms = []
        poll = content_object
        questions = Question.objects.filter(poll=poll)
        for question in questions:
            form = QuestionForm(question, data=request.POST or None, prefix=question.pk)
            forms.append(form)
        captcha_form = CaptchaForm(data=request.POST or None)

        if all( (f.is_valid() for f in forms) ) and captcha_form.is_valid():
            posted_answers = []
            for f in forms:
                posted_answers.extend(f.get_answers())
            submission = Submission(poll=poll)
            submission.save()
            submission.answers = posted_answers
            submission.save()
            return redirect('/poll/%s' % poll.slug)


        else:
            t = loader.get_template("polls/poll_submission.html")
            req_context.update({'poll': poll, 'forms': forms,
                                'captcha_form': captcha_form})
            return t.render(req_context)

frontend.site.register_view(Poll, PollSubmission)


class PollDetail(frontend.FrontendView):
    """Detail view for Polls"""
    name = 'detail'
    verbose_name=_('detailed view of the selected Poll')
    is_default = True
    is_content_view = True

    def get_response(self, request, req_context, options, content_object):
        return views.object_detail(request, req_context, content_object)

frontend.site.register_view(Poll, PollDetail)

