
# cyclope views are usually declared and registered
# in frontend.py files for each app

from django.template import loader, RequestContext
from django.http import Http404, HttpResponse
from django.core.xheaders import populate_xheaders
from django.core.exceptions import ObjectDoesNotExist

from cyclope.utils import template_for_request

def object_detail(request, queryset, inline=False,
        object_id=None, slug=None, slug_field='slug', template_name=None,
        template_name_field=None, template_loader=loader, extra_context=None,
        context_processors=None, template_object_name='object',
        mimetype=None):
    """
    Generic detail of an object.

    Templates: ``<app_label>/<model_name>_detail.html``
    Context:
        object
            the object
    """
    if extra_context is None: extra_context = {}
    model = queryset.model
    if object_id:
        queryset = queryset.filter(pk=object_id)
    elif slug and slug_field:
        queryset = queryset.filter(**{slug_field: slug})
    else:
        raise AttributeError("Generic detail view must be called "
                             "with either an object_id or a slug/slug_field.")
    try:
        obj = queryset.get()
    except ObjectDoesNotExist:
        raise Http404(
            "No %s found matching the query" % (model._meta.verbose_name))
    if not template_name:
        template_name = "%s/%s_detail.html" % (
            model._meta.app_label, model._meta.object_name.lower())
    if template_name_field:
        template_name_list = [getattr(obj, template_name_field), template_name]
        t = template_loader.select_template(template_name_list)
    else:
        t = template_loader.get_template(template_name)
    c = RequestContext(request, {
        template_object_name: obj,
    }, context_processors)
    for key, value in extra_context.items():
        if callable(value):
            c[key] = value()
        else:
            c[key] = value

    if not inline:
        c['host_template'] = template_for_request(request)
        response = HttpResponse(t.render(c), mimetype=mimetype)
        populate_xheaders(request, response, model,
                          getattr(obj, obj._meta.pk.name))
        return response

    else:
        c['host_template'] = 'cyclope/inline_view.html'
        return t.render(c)
