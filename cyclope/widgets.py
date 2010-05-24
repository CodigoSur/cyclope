# *-- coding:utf-8 --*
"""
widgets
-------
"""
from django import forms
from django.utils.safestring import mark_safe
from django.conf import settings
from cyclope import settings as cyc_settings

class WYMEditor(forms.Textarea):
    """Widget to replace a standard textarea with WYMEditor"""
    class Media:
        js = (
            cyc_settings.CYCLOPE_MEDIA_URL +'js/reuse_django_jquery.js',
            cyc_settings.CYCLOPE_MEDIA_URL +'js/jquery.wymeditor.filebrowser.js',
            cyc_settings.CYCLOPE_MEDIA_URL +'js/wymeditor/jquery.wymeditor.pack.js',
        )

    def __init__(self, language=None, attrs=None):
        self.language = language or settings.LANGUAGE_CODE[:2]
        self.attrs = {'class': 'wymeditor'}
        if attrs:
            self.attrs.update(attrs)
        super(WYMEditor, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        rendered = super(WYMEditor, self).render(name, value, attrs)
        return rendered + mark_safe(u'''<script type="text/javascript">
            jQuery('#id_%s').wymeditor({
                updateSelector: '.submit-row input[type=submit]',
                updateEvent: 'click',
                lang: '%s',
                postInitDialog: wymeditor_filebrowser,
            });
            </script>''' % (name, self.language))
