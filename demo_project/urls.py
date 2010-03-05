from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings as django_settings
from django.utils.translation import ugettext as _


###########
# this stuff should be moved to a frontend.py file for each app
# and an autodiscover() should be implemented alla admin.autodiscover()

from cyclope import settings as cyc_settings
from cyclope import site as cyc_site #, ModelDisplay
from django.views.generic.list_detail import object_detail, object_list
from cyclope.apps.articles.models import Article
from cyclope.models import StaticPage

cyc_site.register_view(Article, object_detail,
                       view_name='detail',
                       verbose_name= _('full detail'),
                       default=True)

cyc_site.register_view(StaticPage, object_detail,
                       view_name='detail',
                       verbose_name= _('full detail'),
                       default=True)

cyc_site.register_view(StaticPage, object_list,
                       view_name='list',
                       verbose_name= _('standard listing'),
                       default=False)

############


admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
#    (r'', include('demo_project.website.urls')),
#    (r'^cyclope/', include('cyclope.urls')),

    (r'^admin/', include(admin.site.urls)),
    (r'^%s' % cyc_settings.CYCLOPE_ROOT_URL, include(cyc_site.urls)),
)

if django_settings.DEBUG:
    urlpatterns+= patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': django_settings.MEDIA_ROOT, 'show_indexes': True})
    )

if 'rosetta' in django_settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^rosetta/', include('rosetta.urls')),
    )

    urlpatterns += patterns('',
        url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'admin/login.html'}),
    )
