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

# GET /pictures/new
def pictures_upload(request):
    """ Returns widget's inner HTML to be viewed through an iframe.
        This ensures bootstrap styles isolation."""
    form = MediaWidgetForm()
    return render(request, 'media_widget/pictures_upload.html', {'form': form})

# POST /pictures/create
#TODO use chunks with FileBrowseField?
@require_POST
def pictures_create(request):
    if request.user.is_staff:
        form = MediaWidgetForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            #normalize file name
            image.name = convert_filename(image.name)
            #filesystem save
            path = os.path.join(settings.MEDIA_ROOT, Picture._meta.get_field_by_name("image")[0].directory)
            uploaded_path = handle_file_upload(path, image)
            generate_fb_version(uploaded_path, ADMIN_THUMBNAIL)
            #database save
            picture = Picture(
                name = form.cleaned_data['name'],#TODO or image.name
                description = form.cleaned_data['description'],#TODO or None
                image = uploaded_path
                #TODO user, etc.
            )
            picture.save()
            #TODO associate picture with current Article
            return redirect('pictures-create') #POST/Redirect/GET #TODO or just render with thumbnail?
        else:
            return render(request, 'media_widget/pictures_upload.html', {'form': form})
    else:
        return HttpResponseForbidden()
