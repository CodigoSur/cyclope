# *-- coding:utf-8 --*

from django.utils.translation import ugettext as _

from cyclope.core import frontend
from cyclope import views

from models import *

class MediaDetail(frontend.FrontendView):
    name='detail'
    is_default = True

    def get_http_response(self, request, slug=None, *args, **kwargs):
        return views.object_detail(request, slug=slug,
                                   inline=False, *args, **kwargs)

    def get_string_response(self, request, content_object=None, *args, **kwargs):
        return views.object_detail(request, content_object=content_object,
                                   inline=True, *args, **kwargs)



class PictureDetail(MediaDetail):
    """Detail view of a Picture.
    Returns:
        a string if the view is called from within a region templatetag
        an HttpResponse otherwise
    """
    params = {'template_object_name': 'media',
              'template_name': 'medialibrary/picture_detail.html',
              'queryset': Picture.objects,
             }
    verbose_name=_('detailed view of the selected Picture')

frontend.site.register_view(Picture, PictureDetail())


class SoundTrackDetail(MediaDetail):
    """Detail view of an SoundTrack.
    Returns:
        a string if the view is called from within a region templatetag
        an HttpResponse otherwise
    """
    params = {'template_object_name': 'media',
              'template_name': 'medialibrary/soundtrack_detail.html',
              'queryset': SoundTrack.objects,
             }
    verbose_name=_('detailed view of the selected Audio Track')

frontend.site.register_view(SoundTrack, SoundTrackDetail())


class MovieClipDetail(MediaDetail):
    """Detail view of a MovieClip.
    Returns:
        a string if the view is called from within a region templatetag
        an HttpResponse otherwise
    """
    params = {'template_object_name': 'media',
              'template_name': 'medialibrary/movieclip_detail.html',
              'queryset': MovieClip.objects,
             }
    verbose_name=_('detailed view of the selected Movie Clip')

frontend.site.register_view(MovieClip, MovieClipDetail())


class DocumentDetail(MediaDetail):
    """Detail view of a Document.
    Returns:
        a string if the view is called from within a region templatetag
        an HttpResponse otherwise
    """
    params = {'template_object_name': 'media',
              'template_name': 'medialibrary/document_detail.html',
              'queryset': Document.objects,
             }
    verbose_name=_('detailed view of the selected Document')

frontend.site.register_view(Document, DocumentDetail())


class FlashMovieDetail(MediaDetail):
    """Detail view of a Flash Movie.
    Returns:
        a string if the view is called from within a region templatetag
        an HttpResponse otherwise
    """
    params = {'template_object_name': 'media',
              'template_name': 'medialibrary/flashmovie_detail.html',
              'queryset': FlashMovie.objects,
             }
    verbose_name=_('detailed view of the selected Flash Movie')

    def get_http_response(self, request, slug=None, *args, **kwargs):
        fmovie = FlashMovie.objects.get(slug=slug)
        base = fmovie.flash.url_full[:fmovie.flash.url_full.rfind('/')+1]
        return views.object_detail(request, slug=slug,
                                   inline=False, extra_context={'url_base':base},
                                   *args, **kwargs)

    def get_string_response(self, request, content_object=None, *args, **kwargs):
        base = content_object.flash.url_full[
            :content_object.flash.url_full.rfind('/')+1]
        return views.object_detail(request, content_object=content_object,
                                   inline=True, extra_context={'url_base':base},
                                   *args, **kwargs)

frontend.site.register_view(FlashMovie, FlashMovieDetail())


class RegularFileDetail(MediaDetail):
    """Detail view of a regular file.
    Returns:
        a string if the view is called from within a region templatetag
        an HttpResponse otherwise
    """
    params = {'template_object_name': 'media',
              'template_name': 'medialibrary/regularfile_detail.html',
              'queryset': RegularFile.objects,
             }
    verbose_name=_('detailed view of the selected File')

frontend.site.register_view(RegularFile, RegularFileDetail())


class ExternalContentDetail(MediaDetail):
    """Detail view of external content.
    Returns:
        a string if the view is called from within a region templatetag
        an HttpResponse otherwise
    """
    params = {'template_object_name': 'media',
              'template_name': 'medialibrary/externalcontent_detail.html',
              'queryset': ExternalContent.objects,
             }
    verbose_name=_('detailed view of the selected External Content')

frontend.site.register_view(ExternalContent, ExternalContentDetail())
