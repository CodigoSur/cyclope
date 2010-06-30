# *-- coding:utf-8 --*
"""
widgets
-------
"""
from django import forms
from django.utils.safestring import mark_safe
from django.conf import settings
from django.utils.translation import ugettext as _

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
        editor_toggle = '''
            <p style="clear:both; margin: 0px; padding: 0 0 5px 0;">
            %s:
            <select class="wymtoggle">
                <option value="on">%s</option>
                <option value="off">%s</option>
            </select>
            </p>
            ''' % (_('toggle editor'), _('on'), _('off') )
        rendered = super(WYMEditor, self).render(name, value, attrs)
        return mark_safe(editor_toggle) + rendered + mark_safe(u'''
            <script type="text/javascript">
            jQuery('#id_%s').wymeditor({
                updateSelector: '.submit-row input[type=submit]',
                updateEvent: 'click',
                lang: '%s',
                postInitDialog: wymeditor_filebrowser,
                postInit: function(wym){
                    //Set the 'Toggle' select
                    jQuery('.wymtoggle').change( function() {
                        if(jQuery(this).val() == 'on') {
                            wym.html(jQuery('#id_%s').val());
                            jQuery('.wym_box').show();
                            jQuery('#id_%s').hide();
                            jQuery('.submit-row input[type=submit]').click(function(){wym.update();})
                        } else {
                            wym.update();
                            jQuery('.wym_box').hide();
                            jQuery('#id_%s').show();
                            jQuery('.submit-row input[type=submit]').unbind();
                        }
                    });
                }
            });
            </script>
            '''
            % (name, self.language, name, name, name))
