from django.conf.urls.defaults import *
from cyclope import settings as cyc_settings

# cyclope.autodiscover will search inside installed apps folders
# for frontend.py files and register the views/urls declared.
from cyclope.core import frontend
frontend.autodiscover()

urlpatterns = patterns('',
    (r'^%s' % cyc_settings.CYCLOPE_PREFIX, include(frontend.site.urls)),
)
