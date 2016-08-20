from django.core.management.base import BaseCommand, CommandError
import os
import re
import mimetypes
from cyclope.apps.medialibrary.models import Picture, Document, RegularFile, SoundTrack, MovieClip, FlashMovie
import urllib

class Command(BaseCommand):
    help = 'Finds media in /media/uploads & create their Model objects'
    
    VERSION_NAMES = ('fb_thumb', 'thumbnail', 'small', 'medium', 'big', 'cropped', 'croppedthumbnail', 'slideshow', 'slideshow-background', 'newsletter_teaser', 'carrousel_bootstrap', 'labeled_icon_bootstrap')
    
    def handle(self, *args, **options):
        rootDir = './media/uploads' # TODO argument
        for dirName, subdirList, fileList in os.walk(rootDir):
            print('Found directory: %s' % dirName)
            for fname in fileList:
                if not self.is_version_file(fname):
                    print('\t%s' % fname)
                    self.incorporate(fname, dirName)
                
    def is_version_file(self, filename):
        for version in self.VERSION_NAMES:
            query = version+'\.\w{3,}$'
            if re.search(query, filename):
                return True
        return False
        
    def incorporate(self, filename, path):
        top_level_mime, mime_type = self.guess_type(filename)
        instance = self.create_content_instance(top_level_mime, mime_type, filename, path)
        instance.save()
        print('\t\t importadA %s %s' % (instance.get_object_name().upper(), instance.name) )
        # be happy
        
    def guess_type(self, filename):
        mime_type = mimetypes.guess_type(filename) # 'image/png'
        top_level_mime, mime_type = tuple(mime_type[0].split('/'))
        print('\t\t MIME_TYPE %s' % top_level_mime)
        return (top_level_mime, mime_type)
        
    def create_content_instance(self, top_level_mime, mime_type, filename, path):
        if  top_level_mime == 'image':
            return self.file_to_picture(filename, path)
        elif  top_level_mime == 'audio':
            return self.file_to_sound_track(filename, path)
        elif  top_level_mime == 'video':              
            if mime_type == 'x-flv': 
                return self.file_to_flash_movie(filename, path)
            else:
                return self.file_to_movie_clip(filename, path)
        elif top_level_mime == 'application':
            if mime_type == 'pdf' : 
                return self._wp_file_to_document(filename, path)
            elif mime_type == 'x-shockwave-flash' : 
                return self.file_to_flash_movie(filename, path)
            else :
                return self.file_to_regular_file(filename, path)
        elif top_level_mime == 'text':
            return self.file_to_document(filename, path)
        else: #multipart, example, message, model
            return self.file_to_regular_file(filename, path)

    #TODO if not QUERIES

    def file_name(self, filename):
        return os.path.splitext(filename)[0]

    def path_name(self, path, filename):
        ruta = "%s/%s" % (path, filename)
        ruta = urllib.quote(ruta)
        ruta = ruta.replace('./','/')
        return ruta

    def file_to_picture(self, filename, path):
        return Picture(
            name = self.file_name(filename),
            image = self.path_name(path, filename)
        )

    def file_to_document(self, filename, path):
        return Document(
            name = self.file_name(filename),
            document = self.path_name(path, filename)
        )

    def file_to_regular_file(self, filename, path):
        return RegularFile(
            name = self.file_name(filename),
            file = self.path_name(path, filename)
        )

    def file_to_sound_track(self, filename, path):
        return SoundTrack(
            name = self.file_name(filename),
            audio = self.path_name(path, filename)
        )
    def file_to_movie_clip(self, filename, path):
        return MovieClip(
            name = self.file_name(filename),
            video = self.path_name(path, filename)
        )
    def file_to_flash_movie(self, filename, path):
        return FlashMovie(
            name = self.file_name(filename),
            flash = self.path_name(path, filename)
        )

