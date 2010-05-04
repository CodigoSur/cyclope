# *-- coding:utf-8 --*
"""
core.frontend.sites
-------------------
Frontend views' URL handling.
"""

from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader
from django.conf.urls.defaults import *
from django.utils.translation import ugettext as _
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.contenttypes.models import ContentType
from cyclope.models import BaseContent, Menu, MenuItem, SiteSettings
from cyclope.core.collections.models import Collection, Category

from django.utils import simplejson

from cyclope import settings as cyc_settings

class CyclopeSite(object):
    """Handles frontend display of models.
    """

    def __init__(self):
        self._registry = {}

    def register_view(self, model, view):
        """Register a view for a model.

        Registered views will be available for use in the admin interface.

        Arguments:
            model: a model derived from BaseContent, Menu, MenuItem,
                   core.collections.Collection or core.collections.Category
            view: a view derived from core.frontend.FrontendView
        """

        for base_class in [BaseContent, Menu, MenuItem, Collection, Category]:
            if issubclass(model, base_class):
                break
        else:
            raise TypeError(
                'Cannot register %s models.' % model.__class__)

        if not model in self._registry:
            self._registry[model] = [view]
        else:
            self._registry[model].append(view)


    def get_urls(self):
        from django.conf.urls.defaults import patterns, url
        urlpatterns = patterns('',
            url(r'^$', self.index, name='index'),
            #JSON views for AJAX updating of admin fields
            url(r'^layout_regions_json$', self.layout_regions_json),
            url(r'^registered_region_views_json$', self.registered_region_views_json),
            url(r'^registered_standard_views_json$', self.registered_standard_views_json),
            url(r'^objects_for_ctype_json$', self.objects_for_ctype_json),
        )

        #TODO(nicoechaniz): Fix for multi-site ?
        # url patterns for registered views
        for model, model_views in self._registry.items():
            for view in model_views:
                url_pattern = view.get_url_pattern(model)
                urlpatterns += patterns(
                    '',
                    url(url_pattern,
                    view,
                    name="%s-%s" %
                    (model._meta.object_name.lower(), view.name) )
                )
        # url patterns for menu items
        for item in MenuItem.tree.all():
            if item.custom_url:
                continue
            if item.content_object is not None:
                obj = getattr(item.content_object, item.content_type.model)
                view = self.get_view(obj.__class__, item.content_view)
                urlpatterns += patterns(
                    '', url('^%s$' % item.url, view, {'slug': obj.slug}))
            elif item.content_type is not None:
                mdl = item.content_type.model_class()
                view = self.get_view(mdl, item.content_view)
                urlpatterns += patterns(
                    '', url('^%s$' % item.url, view))
            # this menu item has no content so we will only display the layout
            else:
                urlpatterns += patterns(
                    '', url(r'^%s$' % item.url, self.no_content_layout_view,
                            {'layout': item.layout}))
        return urlpatterns

    def urls(self):
        """URLs for the site's registered frontend views.
        """
        return self.get_urls()
    urls = property(urls)

    def get_default_view_name(self, model):
        """Returns the view name for the default view of the given model
        """
        return [ view.name for view in self._registry[model]
                if view.is_default == True ][0]

    def get_view(self, model, view_name):
        return [ view for view in self._registry[model]
                if view.name == view_name ][0]


#### Site Views ####
#
    def index(self, request):
        """The root Cyclope URL view"""

        #TODO(nicoechaniz): return prettier messages.
        if not cyc_settings.CYCLOPE_SITE_SETTINGS:
            # the site has not been set up in the admin interface yet
            return HttpResponse(_(u'You need to create you site settings'))
        elif cyc_settings.CYCLOPE_DEFAULT_LAYOUT is None:
            return HttpResponse(
                _(u'You need to select a layout for the site'))
        else:
            try:
                home_item = MenuItem.objects.get(site_home=True)
            except ObjectDoesNotExist:
                return HttpResponse(
                    _(u'The site home page has not been set.'))

            if home_item.content_type:
                view = self.get_view(home_item.content_type.model_class(),
                                     home_item.content_view)
                if home_item.content_object:
                    obj = getattr(home_item.content_object, home_item.content_type.model)
                    return view(request, content_object=obj)
                else:
                    return view(request)
            else:
                return self.no_content_layout_view(request, home_item.layout)


    def no_content_layout_view(self, request, layout):
        """View of a layout with no specific content associated"""

        template = 'cyclope/themes/%s/%s' % (
                    cyc_settings.CYCLOPE_CURRENT_THEME,
                    layout.template
                    )
        t = loader.get_template(template)
        c = RequestContext(request)
        return HttpResponse(t.render(c))


### JSON ##

    def layout_regions_json(self, request):
        """View to dynamically update template regions select in the admin."""
        template_filename = request.GET['q']
        theme_name = SiteSettings.objects.get().theme
        theme_settings = getattr(cyc_settings.CYCLOPE_THEMES, theme_name)
        regions = theme_settings.layout_templates[template_filename]['regions']
        regions_data = [{'region_name': '', 'verbose_name': '------'}]
        regions_data.extend([ {'region_name': region_name,
                               'verbose_name': verbose_name}
                            for region_name, verbose_name in regions.items()
                            if region_name != 'content' ])
        json_data = simplejson.dumps(regions_data)
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
                           if view.is_standard_view])

        return simplejson.dumps(views)

    def registered_region_views_json(self, request):
        json_data = self._registered_views(request, region_views=True)
        return HttpResponse(json_data, mimetype='application/json')

    def registered_standard_views_json(self, request):
        json_data = self._registered_views(request)
        return HttpResponse(json_data, mimetype='application/json')

    def objects_for_ctype_json(self, request):
        content_type_id = request.GET['q']
        model = ContentType.objects.get(pk=content_type_id).model_class()
        if hasattr(model, 'tree'):
            objs = model.tree.all()
        else:
            objs = model.objects.all()
        objects = [{'object_id': '', 'verbose_name': '------'}]
        objects.extend([ {'object_id': obj.id,
                        'verbose_name': obj.name}
                       for obj in objs ])
        json_data = simplejson.dumps(objects)
        return HttpResponse(json_data, mimetype='application/json')

#
####

site = CyclopeSite()
