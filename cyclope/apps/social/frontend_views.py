# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.template.loader import select_template
from actstream.models import Action, target_stream, user_stream

from cyclope.core import frontend
from cyclope.templatetags.cyclope_utils import inline_template

class Social(models.Model):
    """Fake model for cyclope frontend view registration"""


class GlobalActivity(frontend.FrontendView):
    name = 'global_activity'
    verbose_name = _('Global activity of the site')
    is_default = True
    is_instance_view = False
    is_region_view = False
    is_content_view = True
    template = "social/actions_list.html"

    def get_response(self, request, req_context, options):
        if request.user.is_authenticated():
            actions = target_stream(request.user) | user_stream(request.user)
        else:
            actions = Action.objects.public()
        # add template variable to action in the form app/model_action_teaser
        # defaulting to 'social/action_teaser.html' if does not exist
        for action in actions:
            if action.action_object:
                specific = inline_template(action.action_object, "action_teaser")
                template = select_template([specific, 'social/action_teaser.html']).name
            else:
                template = 'social/action_teaser.html'
            action.template = template

        return render_to_string(self.template, {
            'object_list': actions,
        }, req_context)

frontend.site.register_view(Social, GlobalActivity)
