#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

import re

from django import forms
from django.conf import settings
from django.forms.util import flatatt
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.utils.html import escape
from django.utils.text import truncate_words
from django.utils.html import conditional_escape
from django.utils.encoding import force_unicode
from django.core.urlresolvers import reverse
from django.contrib.admin.widgets import ForeignKeyRawIdWidget

from cyclope import settings as cyc_settings


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

class CKEditor(forms.Textarea):
    """
    Widget providing CKEditor for Rich Text Editing.
    """
    class Media:
        js = (
            cyc_settings.CYCLOPE_MEDIA_URL + 'ckeditor/ckeditor.js',
        )

    def render(self, name, value, attrs={}):
        language = settings.LANGUAGE_CODE[:2]
        if value is None: value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        return mark_safe(u'''<textarea%s>%s</textarea>
        <script type="text/javascript">

            CKEDITOR.replace("%s",
                {
                    toolbar : // http://docs.cksource.com/CKEditor_3.x/Developers_Guide/Toolbar
                        [
                            ['Cut','Copy','Paste','PasteText'],
                            ['Undo','Redo','-','Find','Replace','-','SelectAll','RemoveFormat'],
                            ['BidiLtr', 'BidiRtl'],
                            '/',
                            ['Bold','Italic','Underline','Strike','-','Subscript','Superscript'],
                            ['NumberedList','BulletedList','-','Outdent','Indent','Blockquote'],
                            ['JustifyLeft','JustifyCenter','JustifyRight','JustifyBlock'],
                            ['Link','Unlink'],
                            ['Image','Flash','Table','HorizontalRule'],
                            '/',
                            ['Styles','Format','Font','FontSize'],
                            ['TextColor','BGColor']
                        ],
                    skin: "v2",
                    height:"291",
                    width:"618",
                    filebrowserUploadUrl : "%s",
                    filebrowserBrowseUrl : "%s",
                    language : "%s",
                }
            );
            // Customizing dialogs
            CKEDITOR.on( 'dialogDefinition', function( ev ){
                    var dialogName = ev.data.name;
                    var dialogDefinition = ev.data.definition;
                    if ( dialogName == 'link' )
                    {
                        dialogDefinition.removeContents( 'advanced' );
                        dialogDefinition.removeContents( 'upload' );
                    }

                    if ( dialogName == 'image' )
                    {
                        dialogDefinition.removeContents( 'advanced' );
                        dialogDefinition.removeContents( 'Upload' );
                    }

                    if ( dialogName == 'flash' )
                    {
                        dialogDefinition.removeContents( 'advanced' );
                        dialogDefinition.removeContents( 'Upload' );
                    }

            });
        </script>''' % (flatatt(final_attrs),
                        conditional_escape(force_unicode(value)),
                        final_attrs['id'],
                        "/", # FIXME http://docs.cksource.com/CKEditor_3.x/Developers_Guide/File_Browser_%28Uploader%29
                        reverse('fb_browse')+'?pop=3', # pop=3 is CKEditor
                        language))


class MultipleWidget(forms.Widget):
    """
    Widget formed by multiple fields. Use with MultipleField.
    """
    def __init__(self, fields, *args, **kwargs):
        self.fields = fields
        super(MultipleWidget, self).__init__(*args, **kwargs)
        self._field_regexp = re.compile("multiple_(.*)")

    def render(self, name, value, *args, **kwargs):
        if value is None or value is u"":
            value = {}
        out_names = ['%s_multiple_%s' % (name, field_name) for field_name in self.fields.keys()]
        out = []
        field_names, fields = self.fields.iterkeys(), self.fields.itervalues()
        for field_name, field, out_name in zip(field_names, fields, out_names):
            out.append(unicode(field.label)+u": " )
            out.append(field.widget.render(out_name, value.get(field_name)))
        return mark_safe(u"<div id='%s_multiple'><ul>" % name + u'\n'.join(out) +u"</ul></div>")

    def value_from_datadict(self, data, files, name):
        out_names = ['%s_multiple_%s' % (name, field_name) for field_name in self.fields.keys()]
        values = {}
        for out_name in out_names:
            field_name = self._field_regexp.search(out_name).groups()[0]
            values[field_name] = data.get(out_name)
        return values
