from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings as django_settings
from django.utils.translation import ugettext as _
from django.conf import settings as django_settings

import cyclope

cyclope.autodiscover()
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
#    (r'', include('demo_project.website.urls')),
#    (r'^cyclope/', include('cyclope.urls')),

    (r'^admin/', include(admin.site.urls)),
    (r'^cyclope/', include(cyclope.site.urls)),
)

if django_settings.DEBUG:
    urlpatterns+= patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': django_settings.MEDIA_ROOT, 'show_indexes': True})
    )

if 'rosetta' in django_settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^rosetta/', include('rosetta.urls')),
    )

    urlpatterns += patterns('',
        url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'admin/login.html'}),
    )
