
###########
# this stuff should be moved to a frontend.py file for each app
# and an autodiscover() should be implemented alla admin.autodiscover()

from django.utils.translation import ugettext as _
from django.views.generic.list_detail import object_detail, object_list

import cyclope.settings as cyc_settings
from cyclope import site as cyc_site

from cyclope.apps.articles.models import Article
from cyclope.models import StaticPage

#cyc_site.register_view(Article, object_detail,
#                       view_name='detail',
#                       verbose_name= _('full detail'),
#                       default=True)

#class StaticPageView(frontend.FrontendView):
#    view_name=''
#    verbose_view_name=_('full detail')
#    is_default = False

cyc_site.register_view(
    StaticPage, object_detail,
    view_name='detail',
    verbose_name= _('full detail'),
    is_default=True,
    view_params = {'queryset': StaticPage.objects,
                   'template_object_name': 'staticpage',
                   'extra_context': {'base_template': 'cyclope/themes/potente/base.html',
                                    'CYCLOPE_THEME_MEDIA_URL': cyc_settings.CYCLOPE_THEME_MEDIA_URL,
                                     }
                   },
#    is_instance_view=True
                       )

cyc_site.register_view(StaticPage, object_list,
                       view_name='list',
                       verbose_name= _('standard listing'),
                       is_default=False,
#                       is_instance_view=False,
                       )

############
