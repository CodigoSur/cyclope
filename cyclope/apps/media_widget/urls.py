from django.conf.urls import patterns, url
from views import pictures_upload, pictures_create

urlpatterns = patterns('',
    url(r'^pictures/new$', pictures_upload, name="pictures-new"),
    url(r'^pictures/create$', pictures_create, name="pictures-create")     
)
