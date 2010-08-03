
from haystack.indexes import *
from haystack import site
import cyclope.apps.medialibrary.models


class BaseMediaIndex(SearchIndex):
    text = CharField(document=True, use_template=True) #template: author, description
    author = CharField(model_attr='author')

class PictureIndex(BaseMediaIndex):
    pass
site.register(cyclope.apps.medialibrary.models.Picture, PictureIndex)

class SoundTrackIndex(BaseMediaIndex):
    pass
site.register(cyclope.apps.medialibrary.models.SoundTrack, SoundTrackIndex)

class MovieClipIndex(BaseMediaIndex):
    pass
site.register(cyclope.apps.medialibrary.models.MovieClip, MovieClipIndex)

class DocumentIndex(BaseMediaIndex):
    pass
site.register(cyclope.apps.medialibrary.models.Document, DocumentIndex)

class FlashMovieIndex(BaseMediaIndex):
    pass
site.register(cyclope.apps.medialibrary.models.FlashMovie, FlashMovieIndex)

class RegularFileIndex(BaseMediaIndex):
    pass
site.register(cyclope.apps.medialibrary.models.RegularFile, RegularFileIndex)

class ExternalContentIndex(BaseMediaIndex):
    pass
site.register(cyclope.apps.medialibrary.models.ExternalContent, ExternalContentIndex)
