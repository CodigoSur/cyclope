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

from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from profiles.utils import get_profile_model

from cyclope.core import frontend
from cyclope.frontend_views import AuthoredMixin



class UserDetail(AuthoredMixin, frontend.FrontendView):
    """Display a user detail
    """
    name='detail'
    verbose_name=_('detailed view of the selected User')
    is_default = True
    is_instance_view = True
    is_region_view = False
    is_content_view = True
    template = "user_profiles/profile_detail.html"

    def get_queryset(self, content_object):
        qs = []
        # get related methods like picture_set, article_set, etc.
        # checking that are BaseContent types
        for related_name in dir(content_object):
            if related_name.endswith('_set'):
                rel_set = getattr(content_object, related_name)
                if rel_set.model in frontend.site.base_content_types:
                    sqs = rel_set.all()
                    # We only want the items that doesn't have author set
                    if hasattr(rel_set.model, "author"):
                        sqs = sqs.filter(author=None)
                    qs.extend(sqs)
        return qs

    def get_response(self, request, req_context, options, content_object):
        if options['show_authored_content']:
            authored_contents_page = self.get_page(request, req_context, options,
                                                   content_object.user)
        else:
            authored_contents_page = None

        return render_to_string(self.template, {
            'inline_view_name': options["inline_view_name"],
            'page': authored_contents_page
        }, req_context)

frontend.site.register_view(get_profile_model(), UserDetail)
