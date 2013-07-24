#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010-2013 Código Sur Sociedad Civil
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


from django.db.models.signals import post_save
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from actstream import action
from cyclope.signals import admin_post_create
from cyclope.apps import medialibrary
from cyclope.apps.articles.models import Article
from cyclope.apps.custom_comments.models import CustomComment
from django.contrib.comments.signals import comment_was_posted
from ratings.signals import vote_was_saved
from ratings.models import Vote


if settings.ACTSTREAM_SETTINGS_ENABLED:

    def creation_activity(sender, request, instance, **kwargs):
        action.send(request.user, verb=_('created'), action_object=instance)

    models = [Article] + medialibrary.models.actual_models

    for model in models:
        admin_post_create.connect(creation_activity, sender=model,
                                  dispatch_uid="%s_creation_activity" % model._meta.object_name.lower())

    def comment_activity(sender, **kwargs):
        instance = kwargs.pop("instance")
        user = instance.user
        target_user = getattr(instance.content_object, "user", None)
        if not kwargs.get("created") or not user:
            return
        action.send(user, verb=_('commented'), action_object=instance,
                    target=target_user)

    post_save.connect(comment_activity, sender=CustomComment,
                      dispatch_uid="custom_comment_creation_activity")


    def rating_activity(sender, **kwargs):
        instance = kwargs.pop("instance")
        user = instance.user
        target_user = getattr(instance.content_object, "user", None)
        if not kwargs.get("created") or not user:
            return
        action.send(user, verb=_('voted'), action_object=instance,
                    target=target_user)

    post_save.connect(rating_activity, sender=Vote, dispatch_uid="vote_activity")


    activities = set(settings.ACTSTREAM_SETTINGS["MODELS"])
    activities.add('custom_comments.customcomment')
    activities.add('ratings.vote')
    [activities.add('%s.%s' % (model._meta.app_label,model._meta.object_name.lower())) for model in models]
    settings.ACTSTREAM_SETTINGS["MODELS"] = list(activities)

