#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010-2012 Código Sur Sociedad Civil.
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
from django.core import urlresolvers
from django.utils.translation import ugettext_lazy as _
from django.contrib.comments.admin import CommentsAdmin
from django.contrib.comments.models import Comment

from models import CustomComment

class CustomCommentsAdmin(CommentsAdmin):
    fieldsets = (
        (None,
           {'fields': ('content_type', 'object_pk')}
        ),
        (_('Content'),
           {'fields': ('user', 'user_name', 'user_email', 'user_url', 'comment')}
        ),
        (_('Metadata'),
           {'fields': ('submit_date', 'ip_address', 'is_public', 'is_removed')}
        ),
     )
    list_display = ('name', "content", "content_url", 'content_type', 'ip_address',
                    'submit_date', 'is_public', 'is_removed')
    list_filter = ('submit_date', 'is_public', 'is_removed')

    def get_actions(self, request):
        base_actions = super(CustomCommentsAdmin, self).actions
        if "flag_comments" in base_actions:
            base_actions.remove("flag_comments")
        actions = super(CustomCommentsAdmin, self).get_actions(request)
        return actions

    def content(self, obj):
        if not obj.object_pk:
            return ""
        admin_url_name = "%s_%s_change" % (obj.content_type.app_label, obj.content_type.name)
        admin_url_name = admin_url_name.replace(" ", "")
        change_url = urlresolvers.reverse('admin:%s' % admin_url_name, args=(obj.content_object.id,))
        return "<a href='%s'>%s</a>" % (change_url, obj.content_object)

    content.allow_tags = True

    def content_url(self, obj):
        if not obj.object_pk:
            return ""
        url = obj.content_object.get_absolute_url()
        return  "<a href='%s'>%s</a>" % (url, url)
    content_url.allow_tags = True

try:
    admin.site.unregister(Comment)
except admin.sites.NotRegistered:
    pass
admin.site.register(Comment, CustomCommentsAdmin)
