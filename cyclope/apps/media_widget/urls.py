from django.conf.urls import patterns, url
from views import pictures_new, pictures_upload, pictures_create, pictures_update, pictures_delete, embed_new, embed_create, library_fetch, pictures_widget, pictures_widget_new, delete_pictures_list

urlpatterns = patterns('',
    # Article's pictures
    # Upload
    url(r'^pictures/new/(?P<article_id>\d+)$', pictures_upload, name="pictures-upload"), #existing article, MUST GO FIRST
    url(r'^pictures/new', pictures_new, name='pictures-new'), # new article
    url(r'^pictures/create/(?P<article_id>\d*)$', pictures_create, name="pictures-create"),
    # Edit
    url(r'^pictures/update/(?P<article_id>\d*)$', pictures_update, name="pictures-update"),
    url(r'^pictures/delete/(?P<article_id>\d*)$', pictures_delete, name="pictures-delete"),
    # Ajax
    url(r'^pictures/widget/article/(?P<article_id>\d+)$', pictures_widget, name="pictures-widget"),
    url(r'^pictures/widget/pictures/(?P<pictures_ids>(\d+,)*)$', pictures_widget_new, name="pictures-widget-new"),
    url(r'^pictures/delete_list/(?P<pictures_ids>(\d+,)*)$', delete_pictures_list, name="pictures-list"),
    
    # Embed media in content
    url(r'^embed/new/(?P<media_type>\w*)$', embed_new, name="embed-new"),
    url(r'^embed/create$', embed_create, name="embed-create"),
    # Ajax
    url(r'^library/(?P<media_type>\w+)$', library_fetch, name="library-fetch")
)
