from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.conf.urls.defaults import *
from django.utils.translation import ugettext as _

from cyclope import settings as cyc_settings

from django.contrib.contenttypes.models import ContentType
from cyclope.models import BaseContent, Menu, MenuItem, SiteSettings
from cyclope.core.collections.models import Collection, Category

from django.utils.importlib import import_module
from django.utils import simplejson

class CyclopeSite(object):
    """
    Handles frontend display of models.
    """
    def __init__(self):
        self._registry = {}
        self._patterns = {}

    def register_view(self, model, view, view_name=None,
                      verbose_name=None, is_default=False,
                      view_params= {}, extra_context={}):

        for base_class in [BaseContent, Menu, MenuItem, Collection, Category]:
            if issubclass(model, base_class):
                break
        else:
            raise TypeError(
                'Cannot register %s models.' % model.__class__)

        #if not issubclass(model, BaseContent)\
        #  and not issubclass(model, Menu)\
        #  and not issubclass(model, MenuItem)\
        #  and not issubclass(model, Collection)\
        #  and not issubclass(model, Category):
        #    raise TypeError(
        #        '%s does not inherit from BaseContent' % model.__class__)

        if not view_name:
            view_name = view.__name__
        if not verbose_name:
            verbose_name = view_name

        view_pattern = model.get_url_pattern()
        view_config = ({'view': view,
                        'view_name': view_name,
                        'verbose_name': verbose_name,
                        'is_default': is_default,
                        'view_params': view_params,
                        'extra_context': extra_context,
                        'view_pattern': view_pattern,
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

        #ToDo: Fix for multi-site
        try:
            site_settings = SiteSettings.objects.get()
            default_layout = site_settings.default_layout
        except:
            default_layout = ''

        for model, model_views in self._registry.items():
            for view_config in model_views:
                try:
                    menu_item = MenuItem.objects.select_related().get(url=req_url)
                except:
                    menu_item = None
                if menu_item:
                    host_template = menu_item.layout.template
                else:
                    host_template = cyc_settings.CYCLOPE_DEFAULT_TEMPLATE
                #if view_config['is_default']:
                #    view_pattern = '%s$' % model.get_url_pattern()
                #else:
                #    view_pattern = '%s/%s$' % (model.get_url_pattern(),
                #                               view_config['view_name'])
                view_pattern = view_config['view_pattern']
                self._patterns[view_pattern] = view_pattern
                view_params = dict(host_template=host_template,
                                   **view_config['view_params'])
                urlpatterns += patterns('',
                                        url(view_pattern, view_config['view'],
                                            view_params)
                                        )
        return urlpatterns

    def urls(self):
        return self.get_urls()
    urls = property(urls)

    def get_default_view_name(self, model):
        return [ view_config for view_config in self._registry[model]
                if view_config['is_default'] == True ][0]['view_name']

    def get_view_config(self, model, view_name):
        return [ view_config for view_config in self._registry[model]
                if view_config['view_name'] == view_name ][0]

#### Site Views ####
#
    def index(self, request):

        if not cyc_settings.CYCLOPE_SITE_SETTINGS:
            # the site has not been set up in the admin interface yet
            return HttpResponse(_(u'You need to create you site settings'))
        else:
            #menu = Menu.objects.get(main_menu=True)
            #main_menu_items = MenuItem.objects.filter(menu=menu)
            #context = {'main_menu': main_menu_items,}
            #try:
            #    menu = Menu.objects.get(main_menu=True)
            #    menu_items = MenuItem.objects.filter(menu=menu)
            #except:
            #    menu_items = []
            #
            #return render_to_response(cyc_settings.CYCLOPE_DEFAULT_TEMPLATE,
            #                          RequestContext(
            #                            request, context,
            #                            )
            #                          )
            return render_to_response(cyc_settings.CYCLOPE_DEFAULT_TEMPLATE,
                                      RequestContext(request)
                                      )


### JSON ##

    def layout_regions_json(self, request):
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
        views.extend([ {'view_name': view_config['view_name'],
                        'verbose_name': view_config['verbose_name']}
                       for view_config in self._registry[model] ])
        json_data = simplejson.dumps(views)
        return HttpResponse(json_data, mimetype='application/json')
#
####

site = CyclopeSite()


##########
## autodiscover() is an almost exact copy of django.contrib.admin.autodiscover()

# A flag to tell us if autodiscover is running.  autodiscover will set this to
# True while running, and False when it finishes.
LOADING = False

def autodiscover():
    """
    Auto-discover INSTALLED_APPS frontend.py modules and fail silently when
    not present.
    This forces an import on them to register frontend views.
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
        import_module('%s.frontend' % app)
#    import cyclope
#    for model in cyclope.site._registry:
    for model in site._registry:
        default_view = [ view_config
                        for view_config in site._registry[model]
                        if view_config['is_default'] == True ]
        if len(default_view) == 0:
            raise(Exception(_(u'No default view set for %s' % model)))
        elif len(default_view) > 1:
            raise(Exception(
                _(u'You can set only one default view for %s' % model)))

    LOADING = False

################
