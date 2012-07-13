from django import template
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType

register = template.Library()

@register.filter
def abuse_report_link(value):
    ct_id = ContentType.objects.get_for_model(value).pk
    obj_id = value.pk
    return reverse("abuse-report", args=(ct_id, obj_id))
