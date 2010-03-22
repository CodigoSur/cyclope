# *-- coding:utf-8 --*
"""Views URL handling and dispatching."""

from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.conf.urls.defaults import *
from django.utils.translation import ugettext as _

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
            url(r'^registered_views_json$', self.registered_views_json),
        )

        #ToDo: Fix for multi-site

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
        return urlpatterns

    def urls(self):
        """The site registered views URLs.
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
                menu = Menu.objects.get(main_menu=True)
                main_menu_items = MenuItem.objects.filter(menu=menu)
            except:
                main_menu_items = []
            context = {'main_menu': main_menu_items,}

            return render_to_response(cyc_settings.CYCLOPE_DEFAULT_TEMPLATE,
                                      RequestContext(
                                        request, context,
                                        )
                                      )

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

    def registered_views_json(self, request):
        content_type_id = request.GET['q']
        model = ContentType.objects.get(pk=content_type_id).model_class()
        views = [{'view_name': '', 'verbose_name': '------'}]
        views.extend([ {'view_name': view_options.name,
                        'verbose_name': view_options.name}
                       for view_options in self._registry[model] ])
        json_data = simplejson.dumps(views)
        return HttpResponse(json_data, mimetype='application/json')
#
####

site = CyclopeSite()
