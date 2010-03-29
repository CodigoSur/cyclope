# *-- coding:utf-8 --*
"""cyclope.frontend_views"""

from django.utils.translation import ugettext as _
from django.template import loader, RequestContext

from cyclope import settings as cyc_settings
from cyclope.core import frontend
from cyclope.core.collections.models import Collection, Category

def custom_list(request, *args, **kwargs):
    host_template = template_for_request(request)
    response = HttpResponse("hola %s" % host_template)
    return response

class CategoryFlatListView(frontend.FrontendView):
    """A list view of the menuitems for the main menu.
    """
    name='category_flat_list'
    verbose_name=_('flat list of category root items')
    is_default = True
    params = {'queryset': Category.objects,
              'template_object_name': 'menu',
              }

    def get_string_response(self, request, slug, *args, **kwargs):
        if slug==None:
            slug = 'novedades'
        category = self.params['queryset'].get(slug=slug)
        elements = []
        for mapping in category.category_maps.all():
            elements.append(mapping.content_object)
            print mapping.content_type.app_label, mapping.content_type.model

        c = RequestContext(request, {'category_maps': category.category_maps.all()})
        t = loader.get_template("collections/category_flat_list.html")
        c['host_template'] = 'cyclope/inline_view.html'
        return t.render(c)

frontend.site.register_view(Category, CategoryFlatListView())
