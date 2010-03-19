from django.utils.translation import ugettext as _
from django.views.generic.list_detail import object_list

from cyclope import site as cyc_site
from cyclope.core import frontend

from cyclope.models import StaticPage


#### testing...
from django.template import loader, RequestContext
from django.http import Http404, HttpResponse
from django.core.xheaders import populate_xheaders
from django.core.paginator import Paginator, InvalidPage
from django.core.exceptions import ObjectDoesNotExist

def object_detail_to_str(request, queryset, host_template=None,
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
    object_id = 1
    if extra_context is None: extra_context = {}
    model = queryset.model
    if object_id:
        queryset = queryset.filter(pk=object_id)
    elif slug and slug_field:
        queryset = queryset.filter(**{slug_field: slug})
    else:
        raise AttributeError("Generic detail view must be called with either an object_id or a slug/slug_field.")
    try:
        obj = queryset.get()
    except ObjectDoesNotExist:
        raise Http404("No %s found matching the query" % (model._meta.verbose_name))
    if not template_name:
        template_name = "%s/%s_detail.html" % (model._meta.app_label, model._meta.object_name.lower())
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
    if not host_template:
        c['host_template'] = 'cyclope/inline_view.html'
    else:
        c['host_template'] = host_template

    if not host_template:
        return t.render(c)
    else:
        response = HttpResponse(t.render(c), mimetype=mimetype)
        populate_xheaders(request, response, model, getattr(obj, obj._meta.pk.name))
        return response


class StaticPageDetailView(frontend.ModelFrontendView):
    view_callable = object_detail_to_str
    view_params = {'queryset': StaticPage.objects,
                   'template_object_name': 'staticpage',
                   },
    name='detail'
    verbose_name=_('full detail')
    is_default = True

    def __call__(self, request, queryset, host_template=None,
        object_id=None, slug=None, slug_field='slug', template_name=None,
        template_name_field=None, template_loader=loader, extra_context=None,
        context_processors=None, template_object_name='object',
        mimetype=None):

        if extra_context is None: extra_context = {}
        model = queryset.model

        object_id = 1

        if object_id:
            queryset = queryset.filter(pk=object_id)
        elif slug and slug_field:
            queryset = queryset.filter(**{slug_field: slug})
        else:
            raise AttributeError("Generic detail view must be called with either an object_id or a slug/slug_field.")
        try:
            obj = queryset.get()
        except ObjectDoesNotExist:
            raise Http404("No %s found matching the query" % (model._meta.verbose_name))
        if not template_name:
            template_name = "%s/%s_detail.html" % (model._meta.app_label, model._meta.object_name.lower())
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
        if not host_template:
            c['host_template'] = 'cyclope/inline_view.html'
        else:
            c['host_template'] = host_template

        if not host_template:
            return t.render(c)
        else:
            response = HttpResponse(t.render(c), mimetype=mimetype)
            populate_xheaders(request, response, model, getattr(obj, obj._meta.pk.name))
            return response


cyc_site.register_view(StaticPage, StaticPageDetailView)

cyc_site.register_view(
    StaticPage, object_detail_to_str,
    view_name='detail',
    verbose_name= _('full detail'),
    is_default=True,
    view_params = {'queryset': StaticPage.objects,
                   'template_object_name': 'staticpage',
                   },
    )

cyc_site.register_view(StaticPage, object_list,
                       view_name='list',
                       verbose_name= _('standard listing'),
                       is_default=False,
                       )

############
