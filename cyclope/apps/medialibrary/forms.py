import os

from django import forms
from django.conf import settings
from django.contrib.contenttypes.models import ContentType

#from filebrowser.functions import handle_file_upload, convert_filename
#from filebrowser.settings import ADMIN_THUMBNAIL

from cyclope.apps.medialibrary.models import Picture
from cyclope.utils import generate_fb_version

class InlinedBaseForm(forms.Form):
    name = forms.CharField()
    ct_id = forms.IntegerField(widget=forms.HiddenInput())

    def get_model_class(self):
        return ContentType.objects.get_for_id(self.cleaned_data["ct_id"]).model_class()

class InlinedMediaForm(InlinedBaseForm):
    file = forms.ImageField()

    def save(self):
        klass = self.get_model_class()
        instance = klass(name=self.cleaned_data["name"])
        abs_path = os.path.join(settings.MEDIA_ROOT,
                   klass._meta.get_field_by_name(instance.media_file_field)[0].directory)
        f = self.cleaned_data['file']
#        f.name = convert_filename(f.name)
#        name = handle_file_upload(abs_path, f)
        setattr(instance, instance.media_file_field, name)
        instance.save()
        return instance

class InlinedPictureForm(InlinedMediaForm):

    def save(self):
        instance = super(InlinedPictureForm, self).save()
#        generate_fb_version(instance.image.path, ADMIN_THUMBNAIL)
        return instance

