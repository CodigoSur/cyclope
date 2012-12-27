#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010-2012 Código Sur Sociedad Civil.
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
core.frontend.sites
-------------------
Frontend views' URL handling.
"""

from django.http import HttpResponse
from django.template import RequestContext, loader
from django.conf.urls import patterns, url
from django.utils.translation import ugettext_lazy as _, ugettext
from django.core.exceptions import ObjectDoesNotExist, ImproperlyConfigured
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.utils import simplejson
from django.db.models import get_model

from cyclope.models import MenuItem, SiteSettings, BaseContent
import cyclope
from cyclope.utils import layout_for_request, LazyJSONEncoder
from cyclope.themes import get_theme

class CyclopeSite(object):
    """Handles frontend display of models.
    """
    def __init__(self):
        self._registry = {}
        self.base_content_types = {}
        self._base_ctype_choices = [('', '------')]
        self._registry_ctype_choices = [('', '------')]

    def register_view(self, model, view_class):
        """Register a view for a model.

        Registered views will be available for use in the admin interface.

        Arguments:
            model: a model.Model that has at least a name attribute
            view_class: a view derived from core.frontend.FrontendView
        """
        view = view_class()
        view.model = model
        if not model in self._registry:
            self._registry[model] = [view]
            ctype = ContentType.objects.get_for_model(model)
            if issubclass(model, BaseContent):
                self.base_content_types[model] = ctype
                self._base_ctype_choices.append((ctype.id,
                                                model._meta.verbose_name))
            self._registry_ctype_choices.append((ctype.id,
                                                model._meta.verbose_name))
        else:
            self._registry[model].append(view)

    def unregister_view(self, model, view_class):
        views = self.get_views(model)
        new_views = [v for v in views if not isinstance(v, view_class)]
        if not new_views:
            self._registry.pop(model, None)
        else:
            self._registry[model] = new_views

    def get_base_ctype_choices(self):
        return sorted(self._base_ctype_choices, key=lambda choice: choice[1])

    def get_registry_ctype_choices(self):
        return sorted(self._registry_ctype_choices, key=lambda choice: choice[1])

    def get_urls(self):
        urlpatterns = patterns('',
            url(r'^$', self.index, name='index'),
            #JSON views for AJAX updating of admin fields
            url(r'^collection_categories_json$', self.collection_categories_json),
            url(r'^layout_regions_json$', self.layout_regions_json),
            url(r'^registered_region_views_json$', self.registered_region_views_json),
            url(r'^registered_standard_views_json$', self.registered_standard_views_json),
            url(r'^objects_for_ctype_json$', self.objects_for_ctype_json),
            url(r'^menu_items_for_menu_json$', self.menu_items_for_menu_json),
            url(r'^options_view_widget_html$', self.options_view_widget_html),
        )

        # url patterns for registered views
        for model, model_views in self._registry.items():
            for view in model_views:
                url_pattern = view.get_url_pattern(model)
                model_name = model._meta.object_name.lower()
                url_name = "%s-%s" % (model_name, view.name)
                urlpatterns += patterns('', url(url_pattern, view, name=url_name))
                if view.is_default:
                    urlpatterns += patterns('', url(url_pattern, view, name=model_name))

        # url patterns for menu items
        urlpatterns.extend(self.get_menuitem_urls())
        return urlpatterns


    def get_menuitem_urls(self):
        urlpatterns = []
        for item in MenuItem.tree.filter(active=True):
            # custom urls are not supposed to be handled by Cyclope
            if item.custom_url:
                continue
            if item.content_object is not None: # if True: content_type should not be None
                obj = item.content_object
                view = self.get_view(obj, item.content_view)
                view_options = item.view_options
                urlpatterns += patterns('', url('^%s$' % item.url, view,
                                                   {'slug': obj.slug,
                                                    'view_options':view_options}))
            elif item.content_type is not None:
                mdl = item.content_type.model_class()
                view = self.get_view(mdl, item.content_view)
                view_options = item.view_options
                urlpatterns += patterns('', url('^%s$' % item.url, view,
                                        {'view_options':view_options}))

            # this menu item has no content so we will only display the layout
            else:
                urlpatterns += patterns('', url(r'^%s$' % item.url,
                                                   self.no_content_layout_view))
        return urlpatterns

    def get_default_view_name(self, model):
        """Returns the view name for the default view of the given model
        """
        return [ view.name for view in self._registry[model]
                if view.is_default == True ][0]

    def get_view(self, obj, view_name):
        """
        Returns the view instance asociated with a model by its name.
        obj could be a model instance or it's class.
        """
        view_ocurrences = [ view for view in self.get_views(obj)
                            if view.name == view_name ]
        # if a view's name has changed this will be False
        # we return the default view to avoid the site from breaking
        if view_ocurrences:
            return view_ocurrences[0]
        else:
            return [ view for view in self.get_views(obj)
                     if view.is_default == True ][0]

    def get_views(self, obj):
        """
        Return a list with the views instances asociated to a model. obj could
        be a model instance or it's class.
        """
        if not isinstance(obj, type):
            obj = obj.__class__
        return self._registry.get(obj, [])

#### Site Views ####

    def index(self, request):
        """The root Cyclope URL view"""

        #TODO(nicoechaniz): return prettier messages.
        if not cyclope.settings.CYCLOPE_SITE_SETTINGS:
            # the site has not been set up in the admin interface yet
            return HttpResponse(ugettext('You need to create you site settings'))

        elif not hasattr(cyclope.settings, 'CYCLOPE_DEFAULT_LAYOUT')\
        or cyclope.settings.CYCLOPE_DEFAULT_LAYOUT is None:
            return HttpResponse(
                ugettext('You need to select a layout for the site'))
        else:
            try:
                home_item = MenuItem.objects.get(site_home=True)
            except ObjectDoesNotExist:
                return HttpResponse(
                    ugettext('The site home page has not been set.'))

            if home_item.content_type:
                view = self.get_view(home_item.content_type.model_class(),
                                     home_item.content_view)
                if home_item.content_object and view.is_instance_view:
                    obj = home_item.content_object
                    view_options = home_item.view_options
                    return view(request, slug=obj.slug, view_options=view_options)
                elif not view.is_instance_view:
                    return view(request)
                else:
                    raise ImproperlyConfigured(ugettext('No content object selected'))
            else:
                return self.no_content_layout_view(request)


    def no_content_layout_view(self, request):
        """View of a layout with no specific content associated"""
        layout = layout_for_request(request)
        template = cyclope.settings.CYCLOPE_THEME_PREFIX + layout.template
        t = loader.get_template(template)
        c = RequestContext(request)
        return HttpResponse(t.render(c))


#### JSON ####

    def collection_categories_json(self, request):
        """Returns the categories that belong to the sellected collection."""
        Collection = get_model('collections','collection')
        Category = get_model('collections','category')
        try:
            pk = int(request.GET['q'])
            collection = Collection.objects.get(pk=pk)
            col_categories = Category.tree.filter(collection=collection)
            categories = [{'category_id': '', 'category_name': '------'}]
            categories.extend([
                    {'category_id': category.id,
                     'category_name': u"%s %s" % ('--' * category.level, category.name)}
                    for category in col_categories])
        except ValueError:
            categories = []
        json_data = simplejson.dumps(categories)
        return HttpResponse(json_data, mimetype='application/json')


    def layout_regions_json(self, request):
        """View to dynamically update template regions select in the admin."""
        template_filename = request.GET['q']
        theme_name = SiteSettings.objects.get().theme
        theme_settings = get_theme(theme_name)
        regions = theme_settings.layout_templates[template_filename]['regions']
        regions_data = [{'region_name': '', 'verbose_name': '------'}]
        regions_data.extend([ {'region_name': region_name,
                               'verbose_name': verbose_name}
                            for region_name, verbose_name
                            in sorted(regions.items(), key=lambda r: r[1])
                            if region_name != 'content' ])
        json_data = simplejson.dumps(regions_data, cls=LazyJSONEncoder)
        return HttpResponse(json_data, mimetype='application/json')

    def _registered_views(self, request, region_views=False):
        content_type_id = request.GET['q']
        model = ContentType.objects.get(pk=content_type_id).model_class()
        views = [{'view_name': '', 'verbose_name': '------'}]
        if region_views:
            views.extend([ {'view_name': view.name,
                            'verbose_name': view.verbose_name}
                           for view in self._registry[model]
                           if view.is_region_view])
        else:
            views.extend([ {'view_name': view.name,
                            'verbose_name': view.verbose_name}
                           for view in self._registry[model]
                           if view.is_content_view])
        json_data = simplejson.dumps(views, cls=LazyJSONEncoder)

        return json_data

    def registered_region_views_json(self, request):
        json_data = self._registered_views(request, region_views=True)
        return HttpResponse(json_data, mimetype='application/json')

    def registered_standard_views_json(self, request):
        json_data = self._registered_views(request)
        return HttpResponse(json_data, mimetype='application/json')

    def menu_items_for_menu_json(self, request):
        id_menu = request.GET['q']

        action_or_id = request.META['HTTP_REFERER'].split('/')[-2]
        if action_or_id == 'add':
            id_menu_item = None
            descendants = []
        else:
            id_menu_item = int(action_or_id)
            menu_item = MenuItem.objects.get(id = id_menu_item)
            descendants = menu_item.get_descendants()

        choices = [{'object_id': '', 'verbose_name': '------'}]

        if not id_menu == '':
            menu_items =  MenuItem.tree.filter(menu = id_menu)

            choices.extend([ {'object_id': item.id,
                            'verbose_name': u'%s %s' % ('---' * item.level, item.name)}
                           for item in menu_items if item.id != id_menu_item and
                                                     item not in descendants])
        json_data = simplejson.dumps(choices)
        return HttpResponse(json_data, mimetype='application/json')

    def objects_for_ctype_json(self, request):
        content_type_id = request.GET['q']
        model = ContentType.objects.get(pk=content_type_id).model_class()
        objects = [{'object_id': '', 'verbose_name': '------'}]
        if hasattr(model, 'tree'):
            objs = model.tree.all()
            objects.extend([ {'object_id': obj.id,
                            'verbose_name': '%s%s' % ('--'*obj.level, obj.name)}
                           for obj in objs ])
        else:
            objs = model.objects.all()
            objects.extend([ {'object_id': obj.id,
                            'verbose_name': obj.name} for obj in objs ])
        json_data = simplejson.dumps(objects)
        return HttpResponse(json_data, mimetype='application/json')

    def options_view_widget_html(self, request):
        """Returns the html with the options of a frontend view"""
        from cyclope.fields import MultipleField
        content_type_name = request.GET.get("content_type_name")
        if content_type_name:
            ct = ContentType.objects.get(name=content_type_name)
        else:
            ct = ContentType.objects.get(pk=request.GET['content_type_id'])
        model = ct.model_class()

        view_name = request.GET['view_name']
        prefix_name = request.GET.get('prefix_name', "")

        frontend_view = self.get_view(model, view_name)
        if frontend_view.options_form is None:
            return HttpResponse("")
        form = frontend_view.options_form()
        view_options = MultipleField(label=_('View options'), form=form, required=False)
        html = view_options.widget.render(name=prefix_name+"view_options",
                                          value=frontend_view.get_default_options())
        return HttpResponse(html)


####

site = CyclopeSite()

def _refresh_site_urls(sender, instance, created, **kwargs):
    "Callback to refresh site url patterns when a MenuItem is modified"
    from django.conf import settings
    import sys
    try:
        return reload(sys.modules[settings.ROOT_URLCONF])
    except KeyError:
        # fails when testing...
        pass
post_save.connect(_refresh_site_urls, sender=MenuItem, dispatch_uid="cyclope.core.frontend.sites")
