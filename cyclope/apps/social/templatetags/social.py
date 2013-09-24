from django import template
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator

import cyclope.utils
from ..utils import steroid_action as _steroid_action

from actstream.models import actor_stream

register = template.Library()

@register.simple_tag
def followers_url(obj):
    ct_id = ContentType.objects.get_for_model(obj).pk
    return reverse('social-followers', None, (ct_id, obj.pk))

@register.simple_tag
def following_url(user):
    return reverse('social-following', None, (user.pk,))

@register.simple_tag
def unfollow_url(actor):
    content_type = ContentType.objects.get_for_model(actor)
    return reverse('actstream_unfollow', kwargs={'content_type_id': content_type.pk,
                                                 'object_id': actor.pk})

@register.simple_tag
def actual_follow_all_url(actor):
    content_type = ContentType.objects.get_for_model(actor)
    return reverse('actstream_follow_all', kwargs={'content_type_id': content_type.pk,
                                                    'object_id': actor.pk})

@register.filter
def steroid_action(action):
    return _steroid_action(action)

@register.filter
def actor_actions(actor, request):
    object_list = [_steroid_action(action) for action in actor_stream(actor)]
    paginator = Paginator(object_list, per_page=10)
    page = cyclope.utils.get_page(paginator, request)
    return page
