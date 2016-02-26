from django.core.urlresolvers import reverse
from django import template

register = template.Library()

@register.simple_tag
def pagination_link(media_type, n, nRows):
    uri = reverse('embed-new', args=(media_type,))
    query_str = "?n="+str(n)+"&nRows="+str(nRows)
    return uri+query_str
    

