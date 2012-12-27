#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2012 Código Sur Sociedad Civil.
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


from django import forms
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from cyclope.core import frontend
from models import CustomComment

class CommentsListOptions(forms.Form):
    limit_to_n_items = forms.IntegerField(label=_('Items to show'), min_value=1,
                                          initial=5)

class CommentsList(frontend.FrontendView):
    """Show a list of the last comments
    """
    name='list'
    verbose_name=_('list of the last site content comments')
    is_default = True
    is_instance_view = False
    is_region_view = True
    options_form = CommentsListOptions

    def get_response(self, request, req_context, options):
        limit = options["limit_to_n_items"]
        qs = CustomComment.objects.filter(is_public=True, is_removed=False)
        comment_list = qs.order_by('-submit_date')[:limit]
        req_context.update({'comment_list': comment_list})
        return render_to_string("comments/comments_list.html",
                                context_instance=req_context)

frontend.site.register_view(CustomComment, CommentsList)
