#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright 2010 Código Sur - Nuestra América Asoc. Civil / Fundación Pacificar.
# All rights reserved.
#
# This file is part of Cyclope.
#
# Cyclope is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Cyclope is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
widgets
-------
"""
from django import forms
from django.utils.safestring import mark_safe
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.html import escape
from django.utils.text import truncate_words
from django.contrib.admin.widgets import ForeignKeyRawIdWidget

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
        editor_toggle = u'''
            <p style="clear:both; margin: 0px; padding: 0 0 5px 0;">
            %s:
            <select class="wymtoggle">
                <option value="on" selected="selected" >%s</option>
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


class ForeignKeyImageRawIdWidget(ForeignKeyRawIdWidget):
    """
    A Widget for displaying ForeignKeys in the "raw_id" interface rather than
    in a <select> box.
    """
    input_type = 'hidden'

    def render(self, name, value, attrs=None):
        if attrs is None:
            attrs = {}
        related_url = '../../../%s/%s/' % (self.rel.to._meta.app_label, self.rel.to._meta.object_name.lower())
        params = self.url_parameters()
        if params:
            url = '?' + '&amp;'.join(['%s=%s' % (k, v) for k, v in params.items()])
        else:
            url = ''
        if not attrs.has_key('class'):
            attrs['class'] = 'vForeignKeyRawIdAdminField' # The JavaScript looks for this hook.
        output = [super(ForeignKeyRawIdWidget, self).render(name, value, attrs)]
        if value:
            output.append(self.thumbnail_for_value(value))
        output.append('<a href="%s%s" class="related-lookup" id="lookup_id_%s" onclick="return showRelatedObjectLookupPopup(this);"> ' % \
            (related_url, url, name))
        output.append('<img src="%simg/admin/selector-search.gif" width="16" height="16" alt="%s" /></a>' % (settings.ADMIN_MEDIA_PREFIX, _('Lookup')))
        return mark_safe(u''.join(output))

    def thumbnail_for_value(self, value):
        key = self.rel.get_related_field().name
        try:
            obj = self.rel.to._default_manager.using(self.db).get(**{key: value})
        except self.rel.to.DoesNotExist:
            return ''
        return obj.thumbnail()
