from django.core.management.base import BaseCommand, CommandError
import os
import re
import mimetypes
from cyclope.apps.medialibrary.models import Picture, Document, RegularFile, SoundTrack, MovieClip, FlashMovie
from filebrowser.base import FileObject
from cyclope.utils import slugify
from datetime import datetime
from django.conf import settings
import errno
from optparse import make_option

class Command(BaseCommand):
    help = 'Finds media in /media/uploads & create their Model objects'
    
    VERSION_NAMES = ('fb_thumb', 'thumbnail', 'small', 'medium', 'big', 'cropped', 'croppedthumbnail', 'slideshow', 'slideshow-background', 'newsletter_teaser', 'carrousel_bootstrap', 'labeled_icon_bootstrap')
    
    #NOTE django > 1.8 uses argparse instead of optparse module, 
    #so "You are encouraged to exclusively use **options for new commands."
    #https://docs.djangoproject.com/en/1.9/howto/custom-management-commands/
    option_list = BaseCommand.option_list + (
        make_option('--dir',
            action='store',
            dest='rootDir',
            default='./media/uploads',
            help='Directory to scan for files, treat, and create objects for them.'
        ),
    )
    
    def handle(self, *args, **options):
        rootDir = options['rootDir']
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
        # sanitize
        name = self.sanitize_filename(filename)
        if filename != name:
            filename = self.correct_filename(path, name, filename)
        # media/type folder structure
        instance = self.create_content_object(top_level_mime, mime_type, filename, self._get_todays_folder(path))
        self.correct_path(path, instance, filename) # always put in today
        # create
        instance.save()
        print('\t\t importar %s %s' % (instance.get_object_name().upper(), instance.name) )
        # be happy
        
    def guess_type(self, filename):
        mime_type = mimetypes.guess_type(filename) # 'image/png'
        top_level_mime, mime_type = tuple(mime_type[0].split('/'))
        print('\t\t MIME_TYPE %s' % top_level_mime)
        return (top_level_mime, mime_type)

    # MIME to MediaType copied from wp2cyclope command        
    def create_content_object(self, top_level_mime, mime_type, name, path):
        # decide
        if  top_level_mime == 'image':
            return self.file_to_picture(name, path)
        elif  top_level_mime == 'audio':
            return self.file_to_sound_track(name, path)
        elif  top_level_mime == 'video':              
            if mime_type == 'x-flv': 
                return self.file_to_flash_movie(name, path)
            else:
                return self.file_to_movie_clip(name, path)
        elif top_level_mime == 'application':
            if mime_type == 'pdf' : 
                return self.file_to_document(name, path)
            elif mime_type == 'x-shockwave-flash' : 
                return self.file_to_flash_movie(name, path)
            else :
                return self.file_to_regular_file(name, path)
        elif top_level_mime == 'text':
            return self.file_to_document(name, path)
        else: #multipart, example, message, model
            return self.file_to_regular_file(name, path)

    #TODO if not QUERIES

    def file_name(self, filename):
        return os.path.splitext(filename)[0]

    def path_name(self, path, filename):
        ruta = "%s/%s" % (path, filename)
        ruta = ruta.replace('./media/','/') # TODO relativizar
        ruta = FileObject(ruta)
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

    def sanitize_filename(self, filename):
        # keep file extension
        m = re.search('(?P<name>.*)(?P<extension>\.\w{3}$)', filename)
        name = m.group('name')
        extension = m.group('extension')
        # truncate name to maximun chars
        name = name[:250]
        # sanitize name
        name = slugify(name)
        #return
        filename = "%s%s" % (name, extension)
        return filename

    def correct_filename(self, path, name, filename):
        "mv name filename"
        src = "%s/%s" % (path, filename)
        dest = "%s/%s" % (path, name)
        os.rename(src, dest)
        print('\t\t mover %s %s' % (src, dest) )
        return name
        
    def correct_path(self, path, instance, filename):
        "mv path/filename new_path/instance.path"
        new_path = '.' + settings.MEDIA_URL + instance.directory[:-1] #--/
        new_path = self._get_todays_folder(new_path)
        src = "%s/%s" % (path, filename)
        dest = "%s/%s" % (new_path, filename)
        self.make_sure_path_exists(new_path)
        os.rename(src, dest)
        print('\t\t mover %s %s' % (src, dest) )
        
    def _get_todays_folder(self, path):
        """
        generate path/year/month directory structure
        ex. /media/pictures/2016/8
        """
        return path+"/{:%Y/%m}".format(datetime.now())
        
    def make_sure_path_exists(self, path):
        try:
            os.makedirs(path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise
