# *-- coding:utf-8 --*
"""
views
-----
Standard views for Cyclope models, to be used by FrontEndView derived objects
which should be declared in a frontend_views.py file for each app."""

# cyclope views are declared and registered
# in frontend.py files for each app

from django.template import loader, RequestContext
from django.http import Http404, HttpResponse
from django.core.xheaders import populate_xheaders
from django.core.exceptions import ObjectDoesNotExist

from cyclope.utils import template_for_request

def object_detail(request, content_object=None, slug=None, queryset=None, inline=False,
        template_name=None, extra_context=None,
        context_processors=None, template_object_name='object',
        mimetype=None):
    """
    Generic detail of an object.

    Arguments:
        ...

    Templates: ``<app_label>/<model_name>_detail.html``
    Context:
        object
            the object
    """
    if extra_context is None: extra_context = {}
    model = queryset.model

    obj = content_object

    if obj is None:
        if queryset and slug:
            try:
                obj = queryset.get(slug=slug)
            except ObjectDoesNotExist:
                raise Http404(
                    "No %s found matching the query" % (model._meta.verbose_name))
        else:
            raise AttributeError("Generic detail view must be called "
                                 "with a content_object or a slug.")
    if not template_name:
        template_name = "%s/%s_detail.html" % (
            model._meta.app_label, model._meta.object_name.lower())
    t = loader.get_template(template_name)

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
