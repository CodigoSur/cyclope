from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.utils.safestring import mark_safe
from django.contrib.contenttypes.models import ContentType
from django.db import models
from cyclope import settings as cyc_settings

from django.forms.widgets import Widget
from django.forms import fields

from cyclope.apps.medialibrary.models import Picture
from django.utils.safestring import mark_safe
from django.utils.html import escape

class MediaWidget(Widget):
    def __init__(self, attrs=None):
        super(MediaWidget, self).__init__(attrs)#,template="media_widget/pictures_button.html")
        
    def render(self, name, value, attrs=None):        
        # svalue [5015, 5016, 5017, 5018, 5019, 5020]
        button = u'<button id="media_widget_button" type="button">Administrar</button>\n'
        thumbs = u''
        for pic_id in value:
            thumbs += Picture.objects.get(pk=pic_id).thumbnail()+'&nbsp;\n'
        #
        widget = button + thumbs
        widget = mark_safe(widget)
        return widget

class MediaWidgetField(fields.MultiValueField):
    pass
    #TODO
    #def __init__(self, fields=(), *args, **kwargs):
    #    super(MediaWidgetField, self).__init__(*args, **kwargs)
    #def validate():
    #    pass
    #def compress(self, data_list):
    #    return ''# if data_list is None else ','.join(data_list)
