from django.core.urlresolvers import reverse
from django import template

register = template.Library()

@register.simple_tag
def pagination_link(widget, param, n, nRows):
    if widget == 'embed':
        uri = reverse('embed-new', args=(param,))# param is media_type
    elif widget == 'pictures':
        uri = reverse('pictures-new', args=(param,))# param is article_id
    else:
        raise MwError("Media Widget pagination tag: Invalid param!")
    query_str = "?n="+str(n)+"&nRows="+str(nRows)
    return uri+query_str
    
class MwError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
