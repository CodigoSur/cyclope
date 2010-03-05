from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.conf.urls.defaults import *

import settings as cyc_settings
#from core.collections import models

from models import BaseContent

class AlreadyRegistered(Exception):
    pass

class ModelDisplay(object):
    """
    Encapsulates frontend display options and functionality for a given model display.
    Each model can be associated with many Displays using site.register()
    """
    def __init__(self, model, name):
        self.model = model
        self.name = name



class CyclopeSite(object):
    """
    Handles frontend display of models.
    """
    def __init__(self):
        self._registry = {}
#        self.root_collections = models.Collection.objects.filter(is_navigation_root=True)
#        self.root_categories = models.Category.objects.filter(is_navigation_root=True)

    def register_view(self, model, view, view_name=None,
                      verbose_name=None, default=False, extra_context={}):

        if not issubclass(model, BaseContent):
            raise TypeError('%s does not inherit from BaseContent' % model.__class__)

        if not view_name:
            view_name = view.__name__
        if not verbose_name:
            verbose_name = view_name
        #if url_pattern is None:
        #    raise AttributeError("register must be called with an url_pattern keyword parameter")
        #else:
        #    url_pattern = url('%s/%s' % (model_url_pattern, view_name))
        #
        #if not default:
        #    url_pattern = url('%s/%s$' % (model.get_url_pattern(), view_name),
        #                      view, model.get_view_params())
        #else:
        #    url_pattern = url('%s$' % model.get_url_pattern(), view, model.get_view_params())

#        url_pattern = url(model.get_url_pattern(), view, model.get_view_params())

        view_config = ({'view': view,
                        'view_name': view_name,
                        'verbose_name': verbose_name,
 #                       'url_pattern': url_pattern,
                        'default': default,
                       })

        #! should check for url conflicts
        if not model in self._registry:
            self._registry[model] = [view_config]
        else:
            self._registry[model].append(view_config)

#if not url_pattern in self._pattern_registry:
#            self._registry[model] = view_config
#            if not model in self._view_registry:
#                self._view_registry[model] = view_config
#            else:
#                self._view_registry[model].append(view_name)
#
#        elif default == True:
#            raise AlreadyRegistered('default view has already been registered')
#        else:
#            raise AlreadyRegistered('%s view has already been registered.' % view_name)
#
#            self._registry[(model,url_pattern)].append(new_view)

    def get_urls(self):
        from django.conf.urls.defaults import patterns, url
        urlpatterns = patterns('',
            url(r'^$', self.index, name=''),
        )

        for model, model_views in self._registry.items():
            for view_config in model_views:
                if view_config['default']:
                    view_pattern = '%s$' % model.get_url_pattern()
                else:
                    view_pattern = '%s/%s$' % (model.get_url_pattern(),
                                               view_config['view_name'])
                urlpatterns += patterns('',
                                        url(view_pattern, view_config['view'],
                                            model.get_view_params())
                                        )
        return urlpatterns

    def urls(self):
        return self.get_urls()
    urls = property(urls)

    def index(self, request):
        return HttpResponse("index")


    #def object_detail(self, request, *args, **kwargs):
    #    return HttpResponse("od")


site = CyclopeSite()


#/collections/coll_slug/cat_slug
#/collections/coll_slug/cat_slug/obj_slug u obj_id
