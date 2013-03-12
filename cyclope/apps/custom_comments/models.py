#!/usr/bin/env python
# -*- coding: UTF-8 -*-
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

from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mass_mail
from django.contrib.comments.managers import CommentManager

from threadedcomments import ThreadedComment
from cyclope.utils import mail_managers


class CustomComment(ThreadedComment):

    subscribe = models.BooleanField(default=False)

    objects = CommentManager()

    def save(self, send_notifications=True, *args, **kwargs):
        created = not self.pk
        super(CustomComment, self).save(*args, **kwargs)

        if created and notification_enabled() and send_notifications:
            self.send_email_notifications()

    def send_email_notifications(self):
        subject = _("New comment posted on '%s'") % self.content_object
        message = self.get_as_text()
        managers_message = message
        if moderation_enabled():
            url = "http://%s%s" % (self.site.domain, reverse('comments-approve',
                                   args=(self.id,)))
            managers_message = _("This comment is moderated!\nYou may approve it " \
                                 "on the following url: %s\n\n") % url + message

        mail_managers(subject, managers_message, fail_silently=True)

        # Send mail to suscribed users of the tree path
        comments = CustomComment.objects.filter(id=self.root_path, subscribe=True)
        if comments:
            messages = [(subject, message, settings.DEFAULT_FROM_EMAIL,
                         [comment.userinfo["email"]]) for comment in comments]
            send_mass_mail(messages, fail_silently=True)

    class Meta:
        verbose_name = _("comment")
        verbose_name_plural = _("comments")



def moderation_enabled():
    from cyclope.utils import get_singleton # Fixme: move out of SiteSettings
    from cyclope.models import SiteSettings
    return get_singleton(SiteSettings).moderate_comments


def notification_enabled():
    from cyclope.utils import get_singleton # Fixme: move out of SiteSettings
    from cyclope.models import SiteSettings
    return get_singleton(SiteSettings).enable_comments_notifications

def comments_allowed():
    from cyclope.utils import get_singleton # Fixme: move out of SiteSettings
    from cyclope.models import SiteSettings
    return get_singleton(SiteSettings).allow_comments
