#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.apps import AppConfig
from actstream import action

class ActivityStreamConfig(AppConfig):
    name = 'cyclope.apps.post_init'
    verbose_name = "cyclope's activity registration"

    # SIGNALS METHODS
    def creation_activity(sender, request, instance, **kwargs):
        action.send(request.user, verb=_('created'), action_object=instance)

    def comment_activity(sender, **kwargs):
        instance = kwargs.pop("instance")
        user = instance.user
        target_user = getattr(instance.content_object, "user", None)
        if not kwargs.get("created") or not user:
            return
        action.send(user, verb=_('commented'), action_object=instance, target=target_user)

    def rating_activity(sender, **kwargs):
        instance = kwargs.pop("instance")
        user = instance.user
        target_user = getattr(instance.content_object, "user", None)
        if not kwargs.get("created") or not user:
            return
        action.send(user, verb=_('voted'), action_object=instance, target=target_user)

    def ready(self):
        # APP REGISTRY READY, IT IS NOW SAFE TO IMPORT MODELS
        from actstream import registry
        from django.contrib.auth.models import User, Group
        from cyclope.apps.custom_comments.models import CustomComment
        from cyclope.apps.articles.models import Article
        from cyclope.signals import admin_post_create
        from django.conf import settings
        from django.db.models.signals import post_save
        # ACSTREAM REGISTRATION
        registry.register(User)
        registry.register(Group)  
        if settings.ACTSTREAM_SETTINGS_ENABLED:
            registry.register(CustomComment)
            # activities.add('ratings.vote') TODO # issue 143
            models = [Article] + medialibrary.models.actual_models
            for model in models:
                registry.register(model)
            # SIGNALS CONNECTION
                admin_post_create.connect(creation_activity, sender=model, dispatch_uid="{}_creation_activity".format(model._meta.object_name.lower()))
            post_save.connect(comment_activity, sender=CustomComment, dispatch_uid="custom_comment_creation_activity")
            #post_save.connect(rating_activity, sender=Vote, dispatch_uid="vote_activity") TODO # issue 143
