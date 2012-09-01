#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2012 Código Sur Sociedad Civil.
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
Based on patches #9976 (https://code.djangoproject.com/ticket/9976)

"""

import re

from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.widgets import ForeignKeyRawIdWidget

from views import do_render_object
from fields import GenericModelChoiceField


generic_script = """
<script type="text/javascript">
function showGenericRelatedObjectLookupPopup(ct_field, triggering_link, url_base) {
    console.log(ct_field);
    console.log(triggering_link);
    var id_name = triggering_link.id.replace(/^lookup_/, '');
    // If ct is inline
    var indx_prefix = ct_field.indexOf("__prefix__")
    if (indx_prefix != -1){
        // get the index of the inline
        var index = triggering_link.id.split("lookup_id_")[1].slice(indx_prefix).split("-")[0];
        ct_field = ct_field.replace("__prefix__", index);
    }
    ct_select = document.getElementById('id_' + ct_field);
    var getCTId = function(ct_select){
        return ct_select.options[ct_select.selectedIndex].value;
    }
    var ct_id = getCTId(ct_select);
    var url = content_types[ct_id];

    function setNewValue(id_name, value){
        var obj = $("#"+id_name);
        obj.attr("newValue", value);
        obj.val(value);
    }

    var ensureRepresentation = function(id_name, ct_select){
        var obj = $("#"+id_name);
        var ct_id = getCTId(ct_select);
        if (obj.attr("value") !== obj.attr("newValue")){
            console.log(ct_id);
            var obj_id = obj.attr("value");
            setNewValue(id_name, ct_id + "-" + obj.attr("value"));
            $.get("/related_admin/render_object/"+ct_id+"/"+obj_id+"/", function(data) {
                obj.siblings(".object-representation").html(data);
            });
        }
    }
    // Yes this is insane but there isn't a robust way to fire an event by a
    // closing window that has a long ajax function inside without blocking
    setInterval(function() {ensureRepresentation(id_name, ct_select); }, 200);

    if (url != undefined) {
        triggering_link.href = url_base + url;
        var rv = showRelatedObjectLookupPopup(triggering_link);
        setNewValue(id_name, "");
        return rv;
    }
    return false;
}

$(".vGenericFKAdminField").css("display", "none");

</script>
"""

class GenericFKWidget(ForeignKeyRawIdWidget):
    def __init__(self, ct_field, cts=None, attrs=None):
        self.ct_field = ct_field
        if cts is None:
            cts = []
        self.cts = cts
        forms.TextInput.__init__(self, attrs)
        self.content_types = """
        <script type="text/javascript">
        var content_types = new Array();
        %s
        </script>
        """ % ('\n'.join(["content_types[%s] = '%s/%s/';" % (ContentType.objects.get_for_model(ct).id,
                                                             ct._meta.app_label, ct._meta.object_name.lower())
                                                             for ct in self.cts]))

    def render(self, name, value, attrs=None):
        # if it is inline build the proper ct_field name
        ct_field = self.ct_field
        if "__prefix__" in name:
            ct_field = re.sub('__prefix__.*', "__prefix__-" + ct_field, name)
        elif re.match('.*\-(\d+\-).*', name):
            ct_field = re.sub('(\d+\-).*', "\g<1>" + ct_field , name)
        self._test_ct_field = ct_field # for testing purposes only
        try:
            actual_object = GenericModelChoiceField.to_python(value)
        except forms.ValidationError:
            actual_object = None
        if attrs is None:
            attrs = {}
        related_url = '../../../'
        params = self.url_parameters()
        if params:
            url = '?' + '&amp;'.join(['%s=%s' % (k, v) for k, v in params.iteritems()])
        else:
            url = ''
        if 'class' not in attrs:
            attrs['class'] = 'vGenericFKAdminField'
        output = [forms.TextInput.render(self, name, value, attrs)]
        output.append('<div class="object-representation float-left">%s</div>' % (do_render_object(actual_object) if actual_object else ""))
        output.append("""%(generic_script)s
            <a href="%(related)s%(url)s" class="related-lookup" id="lookup_id_%(name)s" onclick="return showGenericRelatedObjectLookupPopup('%(ct_field)s', this, '%(related)s%(url)s');"> """
             % {'generic_script': generic_script, 'related': related_url, 'url': url, 'name': name, 'ct_field': ct_field})
        output.append('<img src="%simg/selector-search.gif" width="16" height="16" alt="%s" /></a>' % (settings.STATIC_URL + "admin/", 'Lookup'))
        return mark_safe(u''.join(output) + self.content_types)

    def url_parameters(self):
        return {}
