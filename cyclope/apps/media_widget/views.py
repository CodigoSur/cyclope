from django.shortcuts import render, redirect
from django import forms
from cyclope.apps.medialibrary.models import Picture, BaseMedia, SoundTrack
from cyclope.apps.medialibrary.forms import InlinedPictureForm
from django.views.decorators.http import require_POST
from django.core.urlresolvers import reverse
from forms import MediaWidgetForm, MediaEmbedForm
from filebrowser.functions import handle_file_upload, convert_filename
from django.conf import settings
import os
from filebrowser.settings import ADMIN_THUMBNAIL
from cyclope.utils import generate_fb_version
from django.contrib import messages
from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponse
from cyclope.apps.articles.models import Article
from cyclope.models import RelatedContent
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from models import MediaWidget

###########################
##Article's pictures widget

# GET /pictures/new/article_id
def pictures_upload(request, article_id):
    """ Returns widget's inner HTML to be viewed through an iframe.
        This ensures bootstrap styles isolation."""
    #picture upload
    form = MediaWidgetForm()
    #TODO picture_select and picture_delete forms
    
    #picture selection
    article = Article.objects.get(pk=article_id)
    all_pictures = Picture.objects.all().order_by('-creation_date')
    article_pictures = article.pictures.all()
    pictures = [picture for picture in all_pictures if not picture in article_pictures]
    # pagination
    n, nRows = _paginator_query_string(request)
    paginator = Paginator(pictures, nRows)
    select_page = paginator.page(n)
    #TODO delete_page pagination
        
    # parent admin pictures widget refresh
    refresh_widget = request.session.pop('refresh_widget', False)

    return render(request, 'media_widget/pictures_widget.html', {
        'form': form, 
        'article_id': article_id,
        'refresh_widget': refresh_widget,
        'select_page': select_page,
        'delete_page': article_pictures,
        'n': n,
        'nRows': nRows,
        'param': article_id,
    })

# POST /pictures/create/article_id
@require_POST
def pictures_create(request, article_id):
    if request.user.is_staff:
        form = MediaWidgetForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            #normalize file name
            image.name = convert_filename(image.name)
            #filesystem save
            path = os.path.join(settings.MEDIA_ROOT, 'uploads')
            uploaded_path = handle_file_upload(path, image)
            #thumbnails
            generate_fb_version(uploaded_path, ADMIN_THUMBNAIL)
            #database save
            article = Article.objects.get(pk=article_id)
            picture = Picture(
                name = form.cleaned_data['name'] if form.cleaned_data['name']!='' else image.name,
                description = form.cleaned_data['description'],
                image = uploaded_path,
                user = article.user,
                author = article.author,
                source = article.source
            )
            picture.save()
            
            _associate_picture_to_article(article, picture)
            
            messages.success(request, 'Imagen cargada: '+image.name)
            request.session['refresh_widget'] = True
            
            #POST/Redirect/GET
            return redirect('pictures-new', article_id)
        else:
            # picture selection
            pictures_list = Picture.objects.all().order_by('-creation_date')
            # pagination
            n, nRows = _paginator_query_string(request)
            paginator = Paginator(pictures_list, nRows)
            pagina = paginator.page(n)
            #
            return render(request, 'media_widget/pictures_widget.html', {
                'form': form, 
                'article_id': article_id,
                'pagina': pagina,
                'n': n,
                'nRows': nRows,
                'param': article_id,
            })
    else:
        return HttpResponseForbidden()
        
#POST /pictures/update/article_id
# TODO update multiple pictures
@require_POST
def pictures_update(request, article_id):
    if request.user.is_staff:
        article = Article.objects.get(pk=article_id)
        picture_id = int(request.POST.get('picture_id'))
        picture = Picture.objects.get(pk=picture_id)
        
        _associate_picture_to_article(article, picture)
        
        messages.success(request, 'Imagen seleccionada: '+picture.name)
        request.session['refresh_widget'] = True
        
        return redirect('pictures-new', article_id) # POST/Redirect/GET 
    else:
        return HttpResponseForbidden()

#POST /pictures/delete/article_id
def pictures_delete(request, article_id):
    if request.user.is_staff:
        article = Article.objects.get(pk=article_id)
        picture_id = request.POST['picture_id']
        article.pictures.remove(picture_id)
        #
        messages.warning(request, 'Imagenes eliminadas.')
        request.session['refresh_widget'] = True
    
        return redirect('pictures-new', article_id) # POST/Redirect/GET
    else:
        return HttpResponseForbidden()

#GET /pictures/widget/article_id
def pictures_widget(request, article_id):
    """
    Ajax call to this method refreshes Article Admin's pictures widget thumbnails.
    """
    if request.user.is_staff:
        pictures_list = [picture.id for picture in Article.objects.get(pk=article_id).pictures.all()]
        html = MediaWidget().render("pictures", pictures_list)
        return HttpResponse(html)
    else:
        return HttpResponseForbidden()

####################
##Embed Media Widget

#GET /embed/new
def embed_new(request, media_type):
    if request.user.is_staff:
        # file upload form
        form = MediaEmbedForm()
        # media selection list
        media_list = _fetch_selection_from_library(media_type)
        # pagination
        n, nRows = _paginator_query_string(request)
        paginator = Paginator(media_list, nRows)
        pagina = paginator.page(n)
        # render
        return render(request, 'media_widget/media_widget.html', {
            'form': form,
            'pagina': pagina,
            'n': n,
            'nRows': nRows,
            'media_type': media_type,
            'param': media_type
        })
    else:
        return HttpResponseForbidden()

#POST /embed/create
@require_POST
def embed_create(request):
    if request.user.is_staff:
        form = MediaEmbedForm(request.POST, request.FILES)
        if form.is_valid():
            multimedia = form.cleaned_data['multimedia']
            media_type = form.cleaned_data['media_type']
            if _validate_file_type(media_type, multimedia):
                klass = ContentType.objects.get(model=media_type).model_class()
                instance = klass() # generic instance of media model
                #filesystem save 
                path = os.path.join(settings.MEDIA_ROOT, 'uploads')
                uploaded_path = handle_file_upload(path, multimedia)
                #database save
                instance.name = form.cleaned_data['name'] if form.cleaned_data['name']!='' else multimedia.name
                instance.description = form.cleaned_data['description']
                instance.user = request.user
                setattr(instance, klass.media_file_field, uploaded_path)
                instance.save()
                #response
                return render(request, 'media_widget/media_widget.html', {
                    'form': form,
                    'file_url': instance.media_file,
                    'media_type': media_type,
                })
            else:
                msg = _validation_error_message(multimedia, media_type)
                messages.error(request, msg)
                return render(request, 'media_widget/media_widget.html', {
                    'form': form,
                })
        else:
            return render(request, 'media_widget/media_widget.html', {
                'form': form, 
            })
    else:
        return HttpResponseForbidden()

# GET /library/media_type?n=1&nRows=5
def library_fetch(request, media_type):
    """
    Query Media objects list according to selected media content type.
    Return them as the HTML to render to refresh the area.
    This method could also do pagination and even search.
    """
    if request.user.is_staff:
        # media selection list
        media_list = _fetch_selection_from_library(media_type)
        # pagination
        n, nRows = _paginator_query_string(request)
        paginator = Paginator(media_list, nRows)
        pagina = paginator.page(n)
        # response
        return render(request, 'media_widget/media_select.html', {
            'pagina': pagina,
            'n': n,
            'nRows': nRows,
            'param': media_type,
            'media_type': media_type,
        })
    else:
        return HttpResponseForbidden()

########
#HELPERS

def _associate_picture_to_article(article, picture):
    """Helper method to DRY picture create and update"""
    #add picture to current Article's
    article.pictures.add(picture)
    #article as Picture's related content
    related = RelatedContent(
        self_object = picture,
        other_object = article
    )
    related.save()
    
# what about validating file extensions in javascript?
def _validate_file_type(media_type, multimedia):
    """
    Validate uploaded file MIME type matches intended Content Type.
    Allowed MIME types are different than FileBrowser's because they're the ones allowed by HTML5.
    """
    if media_type == 'picture':
        top_level_mime, mime_type = tuple(multimedia.content_type.split('/'))
        return top_level_mime == 'image' # allow all image types FIXME?
    else:
        if media_type == 'soundtrack':
            allowed_mime_types = ['audio/mpeg', 'audio/ogg', 'audio/wav']
        elif media_type == 'movieclip':
            allowed_mime_types = ['video/mp4', 'video/webm', 'video/ogg']
        elif media_type == 'document':
            allowed_mime_types = ['application/pdf']
        elif media_type == 'flashmovie':
            allowed_mime_types = ['x-shockwave-flash', 'x-flv']
        else:
            return False
        return multimedia.content_type in allowed_mime_types

def _validation_error_message(multimedia, media_type):
    """
    Error message string for MIME type server-side validation
    """
    type_name = {
        'picture': 'Image',
        'soundtrack': 'Audio',
        'movieclip': 'Video',
        'document': 'PDF',
        'flashmovie': 'Flash'
    }
    msg = multimedia.content_type+' is not a valid '+type_name[media_type]+' type!'
    return msg
    
# this function can also be used for search
def _fetch_selection_from_library(media_type):
    """
    Returns media lists filtered by content type
    For selection in Embed Widget search tab.
    Shared by embed_new & select_type actions.
    """
    media_list = ContentType.objects.get(model=media_type).get_all_objects_for_this_type().order_by('-creation_date')
    return media_list
    
def _paginator_query_string(request):
    """
    Interpret ?n=1&nRows=5 query string
    """
    if request.GET.has_key(u'n'):
            n = request.GET[u'n']  #url query string
    else:
        n = 1 #defaults to first
    if request.GET.has_key(u'nRows'):
        nRows = request.GET[u'nRows']  #url query string
    else:
        nRows = 5
    return (n, nRows)
