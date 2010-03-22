# *-- coding:utf-8 --*
import inspect
from sites import site


class FrontendView(object):
    """Parent class for frontend views.

    Class Attributes:
        name: name of the view (must be unique among registered views)
        verbose_name
        params(dict): keyword arguments that will be passed to get_response
        is_default(boolean): is this the default view for the model?
        is_instance_view(boolean): is the view always associated
                                   to an object instance?
    """
    name = ''
    verbose_name = ''
    is_default = False
    template_name = ''
    extra_context = {}
    is_instance_view = True
    params = {}

    def __call__(self, request, *args, **kwargs):
        inline = self.__called_from_region
        if inspect.stack()[1][3] == 'region':
            inline = True
        else:
            inline = False
        if self.params:
            kwargs.update(self.params)
        response = self.get_response(request, inline=inline, *args, **kwargs)
        return response

    def get_response(self, request, *args, **kwargs):
        """Must be overriden by inheriting class and return a proper response.
        """
        raise NotImplementedError()


    def get_url_pattern(self, model):
        if self.is_instance_view:
            return '%s/%s/(?P<slug>.*)/View/%s'\
                    % (model._meta.app_label,
                       model._meta.object_name.lower(), self.name)
        else:
            return '%s/%s/View/%s'\
                    % (model._meta.app_label,
                       model._meta.object_name.lower(), self.name)

    @property
    def __called_from_region(self):
        """Checks if the view is being called from a region templatetag"""
        if inspect.stack()[1][3] == 'region':
            return True
        else:
            return False


##########
# autodiscover() is an almost exact copy of
# django.contrib.admin.autodiscover()

# A flag to tell us if autodiscover is running.  autodiscover will set this to
# True while running, and False when it finishes.
LOADING = False



def autodiscover():
    """Auto-discover INSTALLED_APPS frontend.py modules and fail silently when
    not present.

    This forces an import on them to register frontend views.
    """
    global LOADING
    if LOADING:
        return
    LOADING = True

    import imp
    from django.utils.importlib import import_module
    from django.conf import settings

    for app in settings.INSTALLED_APPS:
        mod = import_module(app)
        try:
            app_path = mod.__path__
        except AttributeError:
            continue
        try:
            imp.find_module('frontend_views', app_path)
        except ImportError:
            continue
        import_module('%s.frontend_views' % app)

    for model in site._registry:
        print model
        default_view = [ view
                        for view in site._registry[model]
                        if view.is_default == True ]
        if len(default_view) == 0:
            raise(Exception(
                _(u'No default view has been set for %s' % model)))
        elif len(default_view) > 1:
            raise(Exception(
                _(u'You can set only one default view for %s' % model)))

    LOADING = False

################
