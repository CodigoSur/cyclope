# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from actstream.models import Action, target_stream, user_stream

from cyclope.core import frontend
import cyclope.utils
from models import Social

class GlobalActivity(frontend.FrontendView):
    name = 'global_activity'
    verbose_name = _("Global activity or user's feed if authenticated")
    is_default = True
    is_instance_view = False
    is_region_view = False
    is_content_view = True
    template = "social/actions_list.html"

    def get_response(self, request, req_context, options):
        actions = self.get_actions(request)
        page = self.build_page(request, actions)
        return render_to_string(self.template, {
            'page': page,
        }, req_context)

    def get_actions(self, request):
        if request.user.is_authenticated():
            actions = target_stream(request.user) | user_stream(request.user)
        else:
            actions = Action.objects.public()
        return actions

    def build_page(self, request, actions):
        paginator = Paginator(actions, per_page=10)
        page = cyclope.utils.get_page(paginator, request)
        return page


class GlobalOnlyActivity(GlobalActivity):
    name = 'global_only_activity'
    verbose_name = _('Global activity of the site')
    is_default = False

    def get_actions(self, request):
        return Action.objects.public()

frontend.site.register_view(Social, GlobalActivity)
frontend.site.register_view(Social, GlobalOnlyActivity)
