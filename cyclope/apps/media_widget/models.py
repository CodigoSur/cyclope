from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.utils.safestring import mark_safe
from cyclope.apps.related_admin import GenericFKWidget
from cyclope.apps.related_admin import GenericModelChoiceField as GMCField
from django.contrib.contenttypes.models import ContentType
from django.db import models
from cyclope import settings as cyc_settings

class MediaWidget(GenericFKWidget):
    def __init__(self, ct_field, cts=None, attrs=None, template=None):
        super(MediaWidget, self).__init__(ct_field, cts, attrs, template="media_widget/pictures_button.html")

class MediaWidgetField(GMCField):
    def __init__(self, queryset, *args, **kwargs):
        self.queryset = queryset
        super(MediaWidgetField, self).__init__(*args, **kwargs)
        
    # displays image thumbnail
    def prepare_value(self, value):
        if value and not value == "None" and not isinstance(value, models.Model):
            value = self.queryset.get(pk=value)
        return super(MediaWidgetField, self).prepare_value(value)
