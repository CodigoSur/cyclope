
###########
# this stuff should be moved to a frontend.py file for each app
# and an autodiscover() should be implemented alla admin.autodiscover()

from django.utils.translation import ugettext as _
from django.views.generic.list_detail import object_detail, object_list

from cyclope import site as cyc_site

from cyclope.apps.articles.models import Article

cyc_site.register_view(
    Article, object_detail,
    view_name='detail',
    verbose_name= _('full detail'),
    is_default=True,
    view_params = {'queryset': Article.objects,
                   'template_object_name': 'article',
                   },
    )
