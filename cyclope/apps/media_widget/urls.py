from django.conf.urls import patterns, url
from views import pictures_upload, pictures_create

urlpatterns = patterns('',
    (r'^pictures/new$', pictures_upload),
    url(r'^pictures/create$', pictures_create, name="pictures-create")     
)
