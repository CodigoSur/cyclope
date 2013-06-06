from django import template
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType

register = template.Library()

@register.simple_tag
def followers_url(obj):
    ct_id = ContentType.objects.get_for_model(obj).pk
    return reverse('social-followers', None, (ct_id, obj.pk))

@register.simple_tag
def following_url(user):
    return reverse('social-following', None, (user.pk,))
