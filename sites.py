from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.conf.urls.defaults import *

from cyclope import settings as cyc_settings

#from core.collections import models

from django.contrib.contenttypes.models import ContentType
from cyclope.models import BaseContent, Menu, MenuItem, SiteSettings

from django.utils.importlib import import_module
from django.utils import simplejson

##########
## autodiscover() is an almost exact copy of django.contrib.admin.autodiscover()

# A flag to tell us if autodiscover is running.  autodiscover will set this to
# True while running, and False when it finishes.
LOADING = False

def autodiscover():
    """
    Auto-discover INSTALLED_APPS frontend.py modules and fail silently when
    not present. This forces an import on them to register any frontend bits they
    may want.
    """
    global LOADING
    if LOADING:
        return
    LOADING = True

    import imp
    from django.conf import settings

    for app in settings.INSTALLED_APPS:
        mod = import_module(app)
        try:
            app_path = mod.__path__
        except AttributeError:
            continue
        try:
            imp.find_module('frontend', app_path)
        except ImportError:
            continue
        import_module("%s.frontend" % app)
    LOADING = False

################

#
#class ModelDisplay(object):
#    """
#    Encapsulates frontend display options and functionality for a given model display.
#    Each model can be associated with many Displays using site.register()
#    """
#    def __init__(self, model, name):
#        self.model = model
#        self.name = name



class CyclopeSite(object):
    """
    Handles frontend display of models.
    """
    def __init__(self):
        self._registry = {}
#        self.root_collections = models.Collection.objects.filter(is_navigation_root=True)
#        self.root_categories = models.Category.objects.filter(is_navigation_root=True)

    def register_view(self, model, view, view_name=None,
                      verbose_name=None, is_default=False, view_params= {}, extra_context={}):

        if not issubclass(model, BaseContent):
            raise TypeError('%s does not inherit from BaseContent' % model.__class__)

        if not view_name:
            view_name = view.__name__
        if not verbose_name:
            verbose_name = view_name

        view_config = ({'view': view,
                        'view_name': view_name,
                        'verbose_name': verbose_name,
                        'is_default': is_default,
                        'view_params': view_params,
                        })

        if not model in self._registry:
            self._registry[model] = [view_config]
        else:
            self._registry[model].append(view_config)


    def get_urls(self):
        from django.conf.urls.defaults import patterns, url
        urlpatterns = patterns('',
            url(r'^$', self.index, name=''),
            url(r'^layout_regions_json$', self.layout_regions_json),
            url(r'^registered_views_json$', self.registered_views_json),
        )

        for model, model_views in self._registry.items():
            for view_config in model_views:
                if view_config['is_default']:
                    view_pattern = '%s$' % model.get_url_pattern()
                else:
                    view_pattern = '%s/%s$' % (model.get_url_pattern(),
                                               view_config['view_name'])
                urlpatterns += patterns('',
                                        url(view_pattern, view_config['view'],
                                            view_config['view_params'])
                                        )
        return urlpatterns

    def urls(self):
        return self.get_urls()
    urls = property(urls)

    def index(self, request):
        menu = Menu.objects.get(pk=1)
        menu_items = MenuItem.objects.filter(menu=menu)
        return render_to_response('cyclope/themes/%s/base.html' \
                % cyc_settings.CYCLOPE_THEME,
                RequestContext(request,
                {'CYCLOPE_THEME_MEDIA_URL': cyc_settings.CYCLOPE_THEME_MEDIA_URL,
                 'menu': menu_items,
                 }))

    def layout_regions_json(self, request):
        template_filename = request.GET['q']
        theme_name = SiteSettings.objects.get().theme
        theme_settings = getattr(cyc_settings.CYCLOPE_THEMES, theme_name)
        regions = theme_settings.layout_templates[template_filename]['regions']
        regions_data = [{'region_name': region_name,
                               'verbose_name': verbose_name}
                                for region_name, verbose_name in regions.items()
                                if region_name != 'content'
                       ]
        json_data = simplejson.dumps(regions_data)
        return HttpResponse(json_data, mimetype='application/json')

    def registered_views_json(self, request):
#        print self._registry
        content_type_id = request.GET['q']
        model = ContentType.objects.get(pk=content_type_id).model_class()
        print "EL MODELO", model
        views = [ {'view_name': view_config['view_name'],
                   'verbose_name': view_config['verbose_name'] }
                  for view_config in self._registry[model] ]
        json_data = simplejson.dumps(views)
        return HttpResponse(json_data, mimetype='application/json')

site = CyclopeSite()


#/collections/coll_slug/cat_slug
#/collections/coll_slug/cat_slug/obj_slug u obj_id
