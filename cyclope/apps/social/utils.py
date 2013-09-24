# -*- coding: utf-8 -*-
from django.template.loader import select_template, get_template
from django.template import TemplateDoesNotExist

from cyclope.templatetags.cyclope_utils import inline_template

def steroid_action(action):
    # add template variable to action in the form app/model_teaser.html
    if action.action_object:
        # the real target object is eg: the object that is comented
        action.real_target = getattr(action.action_object, "content_object", action.action_object)
        action_object_template = inline_template(action.action_object, "action_teaser")
        action.action_object_template = select_template
    elif action.target:
        action.real_target = action.target
    else:
        action.real_target = None
    if action.real_target:
        target_template = inline_template(action.real_target, "teaser")
        try:
            action.target_template = get_template(target_template).name
        except TemplateDoesNotExist:
            action.target_template = None

    action.verb_template = "social/action_teaser_%s.html" % action.verb
    return action
