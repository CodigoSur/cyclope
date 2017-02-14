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

from django.contrib.comments.moderation import CommentModerator, moderator
from django.contrib.comments import signals
import models
from django.contrib.comments.models import CommentFlag

class CustomCommentModerator(CommentModerator):

    email_notification = False

    def moderate(self, comment, content_object, request):
        """
        Return ``True`` if the comment should be moderated (marked
        non-public), ``False`` otherwise.

        """
        if models.moderation_enabled():
            return True
        return False

    def allow(self, comment, content_object, request):
        """
        Return ``True`` if the comment should be allowed, ``False
        otherwise.

        """
        if models.comments_allowed() and \
            getattr(content_object, "allow_comments", True) != "NO":
            return True
        return False

    def post_comment_approval(sender, **kwargs):
        if kwargs['flag'].flag == CommentFlag.MODERATOR_APPROVAL:
            kwargs['comment'].send_subscriptors_notifications()
        
    signals.comment_was_flagged.connect(post_comment_approval, sender=models.CustomComment)
    
