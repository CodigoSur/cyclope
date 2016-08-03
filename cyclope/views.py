#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010-2013 Código Sur Sociedad Civil.
# All rights reserved.
#
# This file is part of Cyclope.
#
# Cyclope is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Cyclope is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
views
-----
Standard views for Cyclope models, to be used by FrontEndView derived objects
which should be declared in a frontend_views.py file for each app."""

# cyclope views are declared and registered
# in frontend.py files for each app

from django.template import loader
from django.http import Http404
from django.core.xheaders import populate_xheaders
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render_to_response
from django.template import RequestContext

from haystack.utils.app_loading import haystack_get_model as get_model
from django.views.generic import DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from cyclope import settings as cyc_settings
from cyclope.utils import get_object_name, get_app_label


def object_detail(request, req_context, content_object, extra_context=None, view_name='detail',
        template_name=None, template_object_name=None):
    """
    Generic detail of an object.
    """
    obj = content_object
    if not template_object_name:
        template_object_name = get_object_name(obj)

    if not template_name:
        template_name = "%s/%s_%s.html" % (get_app_label(obj), get_object_name(obj),
                                           view_name)
    t = loader.get_template(template_name)

    req_context.update({template_object_name: obj})
    if extra_context:
        for key, value in extra_context.items():
            if callable(value):
                req_context[key] = value()
            else:
                req_context[key] = value

    return t.render(req_context)


def object_list(request, req_context, queryset, view_name='list',
                paginate_by=None, page=None, allow_empty=True,
                template_name=None, template_loader=loader,
                extra_context=None, template_object_name=None, mimetype=None):
    """
    Generic list of objects.

    Templates: ``<app_label>/<model_name>_list.html``
    Context:
        object_list
            list of objects
        is_paginated
            are the results paginated?
        results_per_page
            number of objects per page (if paginated)
        has_next
            is there a next page?
        has_previous
            is there a prev page?
        page
            the current page
        next
            the next page
        previous
            the previous page
        pages
            number of pages, total
        hits
            number of objects, total
        last_on_page
            the result number of the last of object in the
            object_list (1-indexed)
        first_on_page
            the result number of the first object in the
            object_list (1-indexed)
        page_range:
            A list of the page numbers (1-indexed).
    """
    if extra_context is None: extra_context = {}
    queryset = queryset._clone()
    if not template_object_name:
        template_object_name = get_object_name(queryset.model)

    if paginate_by:
        paginator = Paginator(queryset, paginate_by, allow_empty_first_page=allow_empty)
        if not page:
            page = request.GET.get('page', 1)
        try:
            page_number = int(page)
        except ValueError:
            if page == 'last':
                page_number = paginator.num_pages
            else:
                # Page is not 'last', nor can it be converted to an int.
                raise Http404
        try:
            page_obj = paginator.page(page_number)
        except InvalidPage:
            raise Http404
        req_context.update({
            '%s_%s' % (template_object_name, view_name): page_obj.object_list,
            'paginator': paginator,
            'page_obj': page_obj,

            # Legacy template context stuff. New templates should use page_obj
            # to access this instead.
            'is_paginated': page_obj.has_other_pages(),
            'results_per_page': paginator.per_page,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
            'page': page_obj.number,
            'next': page_obj.next_page_number(),
            'previous': page_obj.previous_page_number(),
            'first_on_page': page_obj.start_index(),
            'last_on_page': page_obj.end_index(),
            'pages': paginator.num_pages,
            'hits': paginator.count,
            'page_range': paginator.page_range,
            })
    else:
        req_context.update({
            '%s_list' % template_object_name: queryset,
            'paginator': None,
            'page_obj': None,
            'is_paginated': False,
            })
        if not allow_empty and len(queryset) == 0:
            raise Http404
    for key, value in extra_context.items():
        if callable(value):
            req_context[key] = value()
        else:
            req_context[key] = value

    if not template_name:
        model = queryset.model
        template_name = "%s/%s_%s.html" % (get_app_label(model), get_object_name(model), view_name)

    t = template_loader.get_template(template_name)
    return t.render(req_context)


def error_404(request):
    template_name = 'cyclope/themes/%s/404.html' % cyc_settings.CYCLOPE_CURRENT_THEME
    response = render_to_response(template_name,
                                  context_instance = RequestContext(request))
    response.status_code = 404
    return response

def error_500(request):
    template_name = 'cyclope/themes/%s/500.html' % cyc_settings.CYCLOPE_CURRENT_THEME
    response = render_to_response(template_name,
                               context_instance = RequestContext(request))
    response.status_code = 500
    return response

class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)

class ContentDeleteView(DeleteView, LoginRequiredMixin):
    success_url = "/"

    def set_model(self, **kwargs):
        ct = kwargs.pop("content_type")
        app = kwargs.pop("app")
        self.model = get_model(app, ct)

    def get(self, request, *args, **kwargs):
        self.set_model(**kwargs)
        return super(ContentDeleteView, self).get(request, *args, **kwargs)

    def post(self, *args, **kwargs):
        self.set_model(**kwargs)
        return super(ContentDeleteView, self).post(*args, **kwargs)
   
    def get_object(self, queryset=None):
        object = super(ContentDeleteView, self).get_object(queryset)
        if object.user == self.request.user or self.request.user.is_superuser:
            return object
        else:
            raise Http404

# REGION VIEW DELETE

from cyclope.models import RegionView, Layout
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.core.urlresolvers import reverse

def delete_regionview(request, regionview_pk):
    if request.user.is_superuser:
        regionview = RegionView.objects.get(pk=regionview_pk)
        regionview.delete()
        return_to = reverse('admin:cyclope_layout_change', args=(regionview.layout.pk,))
        return HttpResponseRedirect(return_to)
    else:
        return HttpResponseForbidden()
