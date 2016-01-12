from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.utils.safestring import mark_safe
from cyclope.apps.related_admin import GenericFKWidget
from cyclope.apps.related_admin import GenericModelChoiceField as GMCField
from django.contrib.contenttypes.models import ContentType

class MediaWidget(GenericFKWidget):
    def render(self, name, value, attrs):
        out = super(MediaWidget, self).render(name, value, attrs)
        remove_picture = """<div class='remove_picture' onClick="$('#id_%s').val('');$('#id_%s').siblings('.object-representation').empty();">%s</div>""" % (name, name, ugettext(u"Remove"))
        name = "%s_none" % name
        picture_content_type_id = ContentType.objects.get_by_natural_key("medialibrary", "picture").id
        fake_ctfield = "<select id='id_{0}' name='{0}' style='display:none'><option value='{1}'>Picture</option></select>".format(name, picture_content_type_id)
        return mark_safe("<fieldset class='inlined'>" + fake_ctfield + out + remove_picture + "</fieldset>")

    def get_actual_object(self, value):
        try:
            actual_object = MediaWidgetField.to_python(value)
        except forms.ValidationError:
            actual_object = None
        return actual_object

class MediaWidgetField(GMCField):
    def __init__(self, queryset, *args, **kwargs):
        self.queryset = queryset
        super(MediaWidgetField, self).__init__(*args, **kwargs)

    def prepare_value(self, value):
        if value and not value == "None" and not isinstance(value, models.Model):
            value = self.queryset.get(pk=value)
        return super(MediaWidgetField, self).prepare_value(value)
