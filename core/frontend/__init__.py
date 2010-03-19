
############
## This is not being used anywhere.
## It's just an idea that could replace the way views are handled and registered
## in the cyclope.site

class ModelFrontendView(object):
    "Frontend view of a model"
    view_callable = None
    name = ''
    verbose_name = ''
    is_default = False
    view_params = {}

    #def __init__(self, model):
    #    self.model = model

    def __call__(self):
        """
        Must be overriden to implement the actual view.
        """
        return

    #def get_url_pattern(self):
    #    #"""
    #    #This method must be provided by the inheriting class and provide the urlpattern for this view
    #    #"""
    #    return self.model.get_url_pattern()

#class ModelFrontend(object):
#
#    def __init__(self, model):
#        self.model = model
#        self.views = []
#
#    def register(self, view):
#        self.views.append(view)
#
#    def get_urls(self):
#        patterns = []
#        for view in self.views:
#            patterns.append(view.get_url())
#        return patterns

#
#
#############
