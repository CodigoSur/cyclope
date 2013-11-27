#!/usr/bin/env python
# -*- coding: UTF-8 -*-
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

"""
forms
-----
"""

from django import forms
from django.utils.translation import ugettext_lazy as _

from captcha.fields import CaptchaField
from cyclope.apps.polls.models import Submission, Answer


class CaptchaForm(forms.Form):
    captcha = CaptchaField(label=_("Security code"))

class QuestionForm(forms.Form):
    def __init__(self, question, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.question = question
        choices = [(a.id, a.text) for a in Answer.objects.filter(question=question)]
        field_args = {
            "choices": choices,
            "label": question.text.capitalize()
        }


        if question.allow_multiple_answers:
            self.fields['answers'] = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), **field_args)
        else:
            self.fields['answers'] = forms.ChoiceField(widget=forms.RadioSelect(), **field_args)

    def get_answers(self):
        answer_ids = self.cleaned_data['answers']

        # if not multiple_answers
        # TODO: this is hacky. look for a better solution
        if not type(answer_ids) == list:
            answer_ids = [answer_ids]

        return answer_ids

    class Meta:
        model = Submission

