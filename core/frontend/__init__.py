
class FrontendView(object):
    """
    Parent class for frontend views that will be registered in cyclope.site
    """
    name = ''
    verbose_name = ''
    is_default = False
    template_name = ''
    extra_context = {}
    is_instanceview = True
    params = {}

    def __call__(self, request, *args, **kwargs):
        if self.params:
            kwargs.update(self.params)
        response = self.get_response(request, *args, **kwargs)
        return response

    def get_response(self, request, *args, **kwargs):
        raise NotImplementedError()

