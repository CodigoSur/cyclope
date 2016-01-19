from django.shortcuts import render, redirect
from django import forms
from cyclope.apps.medialibrary.models import Picture
from cyclope.apps.medialibrary.forms import InlinedPictureForm
from django.views.decorators.http import require_POST
from django.core.urlresolvers import reverse
from forms import MediaWidgetForm
from filebrowser.functions import handle_file_upload, convert_filename
from django.conf import settings
import os
from filebrowser.settings import ADMIN_THUMBNAIL
from cyclope.utils import generate_fb_version
from django.contrib import messages
from django.http import HttpResponseBadRequest, HttpResponseForbidden
from cyclope.apps.articles.models import Article
from cyclope.models import RelatedContent

# GET /pictures/new/article_id
def pictures_upload(request, article_id):
    """ Returns widget's inner HTML to be viewed through an iframe.
        This ensures bootstrap styles isolation."""
    #picture upload
    form = MediaWidgetForm()
    #picture selection
    pictures_list = Picture.objects.all().order_by('-creation_date')
    #TODO MediaWidgetSelectForm to select multiple pictures
    return render(request, 'media_widget/pictures_upload.html', {
        'form': form, 
        'article_id': article_id,
        'pictures_list': pictures_list
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
            path = os.path.join(settings.MEDIA_ROOT, Picture._meta.get_field_by_name("image")[0].directory)
            uploaded_path = handle_file_upload(path, image)
            #thumnnails
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
            #POST/Redirect/GET
            return redirect('pictures-new', article_id)
        else:
            #picture selection
            pictures_list = Picture.objects.all().order_by('-creation_date')
            return render(request, 'media_widget/pictures_upload.html', {
                'form': form, 
                'article_id': article_id,
                'pictures_list': pictures_list
            })
    else:
        return HttpResponseForbidden()
        
#POST /pictures/update/article_id
@require_POST
def pictures_update(request, article_id):
    if request.user.is_staff:
        article = Article.objects.get(pk=article_id)
        picture_id = int(request.POST.get('picture_id'))
        picture = Picture.objects.get(pk=picture_id)
        _associate_picture_to_article(article, picture)
        messages.success(request, 'Imagen seleccionada: '+picture.name)
        return redirect('pictures-new', article_id) # POST/Redirect/GET 
    else:
        return HttpResponseForbidden()
        
#HELPERS
def _associate_picture_to_article(article, picture):
    """Helper method to DRY picture create and update"""
    #associate picture with current Article
    article.picture = picture
    article.save()
    #article as Picture's related content
    related = RelatedContent(
        self_object = picture,
        other_object = article
    )
    related.save()
