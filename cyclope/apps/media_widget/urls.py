from django.conf.urls import patterns
from views import pictures_upload

urlpatterns = patterns('',
    (r'^pictures/new$', pictures_upload),         
)
