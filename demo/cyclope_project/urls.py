#!/usr/bin/env python

from django.conf.urls.defaults import *
from django.conf import settings as django_settings
from django.utils.translation import ugettext as _
from django.conf import settings as django_settings
from registration.views import register
from cyclope.forms import UserProfileForm
from cyclope.core.captcha_contact_form.forms import  \
                                       AdminSettingsContactFormWithCaptcha

from cyclope import settings as cyc_settings

# autodiscover will search inside installed apps folders
# for frontend_views.py files and register the views/urls declared.
from cyclope.core import frontend
frontend.autodiscover()

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/filebrowser/', include('filebrowser.urls')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    url(r'^admin_tools/', include('admin_tools.urls')),

    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^captcha/', include('captcha.urls')),
    (r'^tagging_autocomplete/', include('tagging_autocomplete.urls')),
    url(r'^accounts/register/$', 'registration.views.register',
        {'backend': 'cyclope.registration_backends.CaptchaBackend'},
        name='registration_register'),
    (r'^accounts/', include('registration.backends.default.urls')),
    (r'^profiles/create/$', 'profiles.views.create_profile',
     {'form_class': UserProfileForm}),
    (r'^profiles/edit/$', 'profiles.views.edit_profile',
     {'form_class': UserProfileForm}),

    (r'^profiles/', include('profiles.urls')),

    url(r'^contact/$', 'contact_form.views.contact_form',
        {'form_class': AdminSettingsContactFormWithCaptcha},
        name='contact_form'),
    (r'^contact/', include('contact_form.urls')),
    (r'^%s' % cyc_settings.CYCLOPE_PREFIX,
     include(frontend.site.get_urls())),
)

if django_settings.DEBUG:
    urlpatterns+= patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': django_settings.MEDIA_ROOT, 'show_indexes': True})
    )

    import os, feincms
    feincms_root = os.path.join(feincms.__path__[0], 'media/feincms/')
    urlpatterns+= patterns('',
        url(r'^feincms_media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': feincms_root, 'show_indexes': True})
    )


if 'rosetta' in django_settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^rosetta/', include('rosetta.urls')),
    )

    urlpatterns += patterns('',
        url(r'^accounts/login/$', 'django.contrib.auth.views.login',
            {'template_name': 'admin/login.html'}),
    )
