from django.shortcuts import render
from django import forms
from cyclope.apps.medialibrary.models import Picture
from cyclope.apps.medialibrary.forms import InlinedPictureForm
from django.views.decorators.http import require_POST
from django.core.urlresolvers import reverse
from forms import MediaWidgetForm

# GET /pictures/new
def pictures_upload(request):
    """ Returns widget's inner HTML to be viewed through an iframe.
        This ensures bootstrap styles isolation."""
    form = MediaWidgetForm()
    return render(request, 'media_widget/pictures_upload.html', {'form': form})

# POST /pictures/create
@require_POST
def pictures_create(request):
    if request.user.is_staff:
        form = MediaWidgetForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save()
            #TODO associate image with Picture's FileBrowseField
            return HttpResponseRedirect(reverse('pictures-create')) #POST/Redirect/GET
        else:
            return render(request, 'media_widget/pictures_upload.html', {'form': form})
    else:
        return HttpResponseForbidden()
