from django.shortcuts import render

def pictures_upload(request):
    """Returns widget's inner HTML to be viewed through an iframe.
    This ensures bootstrap styles isolation."""
    return render(request, 'media_widget/pictures_upload.html')
