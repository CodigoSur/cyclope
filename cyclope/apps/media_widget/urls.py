from django.conf.urls import patterns, url
from views import pictures_upload, pictures_create, pictures_update, pictures_delete, embed_new, embed_create, library_fetch

urlpatterns = patterns('',
    # article pictures
    url(r'^pictures/new/(?P<article_id>\d+)$', pictures_upload, name="pictures-new"),
    url(r'^pictures/create/(?P<article_id>\d+)$', pictures_create, name="pictures-create"),
    url(r'^pictures/update/(?P<article_id>\d+)$', pictures_update, name="pictures-update"),
    url(r'^pictures/delete/(?P<article_id>\d+)$', pictures_delete, name="pictures-delete"),
    # embedded multimedia #TODO article_id?
    url(r'^embed/new$', embed_new, name="embed-new"),
    url(r'^embed/create$', embed_create, name="embed-create"),
    url(r'^library/(?P<media_type>\w+)$', library_fetch, name="library-fetch")
)
