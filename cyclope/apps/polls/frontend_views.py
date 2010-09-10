#!/usr/bin/env python
# -*- coding: UTF-8 -*-
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


from django.utils.translation import ugettext_lazy as _
from django.template import loader, RequestContext
from django.http import Http404, HttpResponse
from django.forms.formsets import formset_factory
from django.shortcuts import redirect

from cyclope.core import frontend
from cyclope.utils import template_for_request
from cyclope import views

from models import Poll, Submission, Question
from forms import QuestionForm, CaptchaForm

class PollSubmissionView(frontend.FrontendView):
    """Show or process a Poll Submission form"""

    name = 'submission'
    verbose_name=_('Poll submission form')

    def get_http_response(self, request, slug=None, *args, **kwargs):
        forms = []
        
        poll = Poll.objects.get(slug=slug)
        questions = Question.objects.filter(poll=poll)
        for question in questions:
            form = QuestionForm(question, data=request.POST or None, prefix=question.pk)
            forms.append({'question': question.text, 'form': form})
        captcha_form = CaptchaForm(data=request.POST or None)

        if all( (d['form'].is_valid() for d in forms) ) and captcha_form.is_valid():
            posted_answers = []
            for d in forms:
                posted_answers.extend(d['form'].get_answers())
            submission = Submission(poll=poll)
            submission.save()
            print posted_answers
            submission.answers = posted_answers
            submission.save()
            return redirect('/poll/%s' % poll.slug)
            

        else:
            t = loader.get_template("polls/poll_submission.html")
            c = RequestContext(request,
                               {'host_template': template_for_request(request),
                                'poll': Poll.objects.get(slug=slug),
                                'forms': forms,
                                'captcha_form': captcha_form,
                                })
            return HttpResponse(t.render(c))

frontend.site.register_view(Poll, PollSubmissionView())


class PollDetailView(frontend.FrontendView):
    """Detail view for Polls"""
    name = 'detail'
    verbose_name=_('detailed view of the selected Poll')
    is_default = True
    params = {'queryset': Poll.objects,
              'template_object_name': 'poll',
             }

    def get_http_response(self, request, slug=None, *args, **kwargs):
        return views.object_detail(request, slug=slug,
                                   inline=False, *args, **kwargs)
    
frontend.site.register_view(Poll, PollDetailView())

