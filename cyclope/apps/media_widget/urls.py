from django.conf.urls import patterns, url
from views import pictures_upload, pictures_create

urlpatterns = patterns('',
    url(r'^pictures/new/(?P<article_id>\d+)$', pictures_upload, name="pictures-new"),
    url(r'^pictures/create/(?P<article_id>\d+)$', pictures_create, name="pictures-create")     
)
