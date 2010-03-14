
############
## This is not being used anywhere.
## It's just an idea that could replace the way views are handled and registered
## in the cyclope.site

class FrontendView(object):

    def __init__(self, name, verbose_name, is_default, is_instance_view):
        self.name = name
        self.verbose_name = verbose_name
        self.is_default = is_default
        self.is_instance_view = is_instance_view

    def __call__(self):
        """
        Must be overriden to implement the actual view.
        """
        return

    def get_url(self):
        """
        This method must be provided by the inheriting class and provide the urlpattern for this view
        """
        return

class ModelFrontend(object):
    view_name=''
    verbose_view_name=_('full detail')
    is_default = False

    def __init__(self, model):
        self.model = model
        self.views = []

    def register(self, view):
        self.views.append(view)

    def get_urls(self):
        patterns = []
        for view in self.views:
            patterns.append(view.get_url())
        return patterns
#
#
#############
