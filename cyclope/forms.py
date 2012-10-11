#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010-2012 Código Sur Sociedad Civil.
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
forms
-----
"""

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.admin.widgets import AdminTextareaWidget

from mptt.forms import TreeNodeChoiceField

from cyclope.core.frontend import site
from cyclope.models import MenuItem, RelatedContent, SiteSettings, Layout, \
                            RegionView
from cyclope.fields import MultipleField
from cyclope.themes import get_all_themes, get_theme
from cyclope.apps.related_admin import GenericFKWidget, GenericModelForm
from cyclope.apps.related_admin import GenericModelChoiceField as GMCField



class AjaxChoiceField(forms.ChoiceField):
    """ChoiceField that always returns true for validate().
    """
    # we always return true because we don't know what choices were available
    # at submit time, because they were populated through AJAX.
    # we use this in cases where providing all the posible choices at init time
    # would be too expensive
    #TODO(nicoechaniz): generate valid choices at init time to avoid this hack when possible?
    def validate(self, value):
        return True


class RelatedContentForm(GenericModelForm):

    other_object = GMCField(label='object', widget=GenericFKWidget('other_type',
                                                   cts=site.base_content_types))

    def __init__(self, *args, **kwargs):
        super(RelatedContentForm, self).__init__(*args, **kwargs)
        self.fields['other_type'].choices = site.get_base_ctype_choices()

    class Meta:
        model = RelatedContent
        fields = ('order', 'other_type', 'other_object')


class ViewOptionsFormMixin(object):
    options_field_name = 'view_options'
    view_field_name = 'content_view'
    field_names = []
    model = None

    def set_initial_view_options(self, obj, model):
        view_name = getattr(obj, self.view_field_name)
        view = site.get_view(model, view_name)

        self.fields[self.options_field_name] = MultipleField(form=view.options_form,
                                                             required=False)

        initial_options = self.fields[self.options_field_name].initial
        actual_options = getattr(obj, self.options_field_name)
        self.initial[self.options_field_name] = actual_options or initial_options

    def get_view(self, values):
        return site.get_view(self.model, values[self.view_field_name])

    def clean_view_options(self):
        # Retrieve content_view and content_type of current data
        values = {}
        field_names = self.field_names
        for name in field_names:
            field, widget = self.fields[name], self.fields[name].widget
            values[name] = widget.value_from_datadict(self.data, None,
                                                      self.add_prefix(name))
            values[name] = field.clean(values[name])
        cleaned_value = {}
        if all(values.values()):
            view = self.get_view(values)
            # Now we need to instance view_options field with the viw of the current
            # form, and clean it.
            self.fields[self.options_field_name] = MultipleField(form=view.options_form,
                                                        required=False)
            field = self.fields[self.options_field_name]
            value = field.widget.value_from_datadict(self.data, None,
                                                     self.add_prefix(self.options_field_name))

            cleaned_value = field.clean(value, validate=True)
        return cleaned_value


class MenuItemAdminForm(GenericModelForm, ViewOptionsFormMixin):
    # content_view choices get populated through javascript
    # when a template is selected
    content_view = AjaxChoiceField(label=_('View'), required=False)
    content_object = GMCField(label=_('Content object'), required=False,
                              widget=GenericFKWidget("content_type",
                                                     cts=site._registry.keys()))
    parent = TreeNodeChoiceField(label=_('Parent'), queryset=MenuItem.tree.all(),
                                 required=False)
    view_options = MultipleField(label=_('View options'), form=None, required=False)


    field_names = ['content_type', "content_view"]

    def __init__(self, *args, **kwargs):
        super(MenuItemAdminForm, self).__init__(*args, **kwargs)
        if self.instance.id is not None:
            # chainedSelect will show the selected choice
            # if it is present before filling the choices through AJAX
            menu_item = MenuItem.objects.get(id=self.instance.id)
            selected_view = menu_item.content_view
            self.fields['content_view'].choices = [(selected_view,
                                                    selected_view)]
            if menu_item.content_type:
                model = menu_item.content_type.model_class()
                self.set_initial_view_options(menu_item, model)

        self.fields['content_type'].choices = site.get_registry_ctype_choices()

    def get_view(self, values):
        return site.get_view(values['content_type'].model_class(),
                              values[self.view_field_name])

    def clean(self):
        data = self.cleaned_data
        data['content_object'] = data.get('content_object')

        if data['custom_url'] and (data.get('content_type')
                                   or data.get('content_object')
                                   or data.get('content_view')):
            raise ValidationError(
                _(u'You can not set a Custom URL for menu entries \
                    with associated content'))

        else:
            if data['content_type']:
                if data['content_view'] == '' or not data['content_view']:
                    raise(ValidationError(
                        _(u'You need to select a content view')))
                else:
                    view = site.get_view(data['content_type'].model_class(),
                                         data['content_view'])
                    if view.is_instance_view and data['content_object'] is None:
                        raise(ValidationError(
                            _(u'The selected view requires a content object')))
                    elif not view.is_instance_view:
                        # if not an instance it does not need a content object
                        if data['content_object'] is not None:
                            data['content_object'] = None

        return super(MenuItemAdminForm, self).clean()

    class Meta:
        model = MenuItem


class SiteSettingsAdminForm(forms.ModelForm):
    theme = forms.ChoiceField(label=_('Theme'),
        choices=[(theme_name,  theme.verbose_name)
                 for theme_name, theme in get_all_themes().iteritems()],
        required=True)

    def __init__(self, *args, **kwargs):
        super(SiteSettingsAdminForm, self).__init__(*args, **kwargs)
        self.fields["keywords"].widget = AdminTextareaWidget()
        self.fields["description"].widget = AdminTextareaWidget()
        self.fields['rss_content_types'].choices = site.get_base_ctype_choices()

        #TODO(diegoM): I don't like this...
        if ('', '------') in self.fields['rss_content_types'].choices:
            self.fields['rss_content_types'].choices.remove(('', '------'))

    class Meta:
        model = SiteSettings


class LayoutAdminForm(forms.ModelForm):
    template = forms.ChoiceField(label=_('Template'), required=True)

    def __init__(self, *args, **kwargs):
        super(LayoutAdminForm, self).__init__(*args, **kwargs)

        try:
            theme_name = SiteSettings.objects.get().theme
        except:
            return

        theme = get_theme(theme_name)
        tpl_choices = [(tpl, tpl_settings['verbose_name'])
                       for tpl, tpl_settings
                       in theme.layout_templates.items()]

        self.fields['template'].choices = tpl_choices

    class Meta:
        model = Layout


class RegionViewInlineForm(forms.ModelForm, ViewOptionsFormMixin):

    # Choices for these fields get populated through javascript/JSON.
    region = AjaxChoiceField(label=_('Region'), required=False)
    content_view = AjaxChoiceField(label=_('View'), required=False)
    object_id = AjaxChoiceField(label=_('Content object'), required=False)
    view_options = MultipleField(label=_('View options'), form=None, required=False)

    field_names = ['content_type', "content_view"]

    def __init__(self, *args, **kwargs):
        super(RegionViewInlineForm, self).__init__(*args, **kwargs)
        if self.instance.id is not None:
            # chainedSelect.js will show the selected choice
            # if it is present before filling the choices through AJAX
            # so we set all choices here at __init__ time
            region_view = RegionView.objects.get(id=self.instance.id)

            if region_view.region:
                selected_region = region_view.region
                self.fields['region'].choices = [(selected_region,
                                                  selected_region)]
            if region_view.content_view:
                selected_view = region_view.content_view
                self.fields['content_view'].choices = [(selected_view,
                                                        selected_view)]
            if region_view.content_type:
                model = region_view.content_type.model_class()
                self.set_initial_view_options(region_view, model)

            if region_view.content_object:
                content_object = region_view.content_object
                self.fields['object_id'].choices = [(content_object.id,
                                                        content_object.name)]

        self.fields['content_type'].choices = site.get_registry_ctype_choices()

    def get_view(self, values):
        return site.get_view(values['content_type'].model_class(),
                              values[self.view_field_name])

    def clean(self):
        #TODO(nicoechaniz): this whole form validation could be simplified if we were not using our custom AjaxChoiceField and fields were actually marked as not null in the model definition. The problem is that the standard form validation will check for valid choices, so we should set choices to valid ones for each choicefield at form init time.

        data = self.cleaned_data
        if not data['DELETE']:
            if data['object_id'] == '':
                data['object_id'] = None

            if not data['content_type']:
                raise(ValidationError(_(u'Content type can not be empty')))

            else:
                if not data['region']:
                    raise(ValidationError(_(u'You need to select a region')))
                if data['content_view'] == '' or not data['content_view']:
                    raise(ValidationError(
                        _(u'You need to select a content view')))
                else:
                    view = site.get_view(data['content_type'].model_class(),
                                         data['content_view'])
                    if view.is_instance_view and data['object_id'] is None:
                        raise(ValidationError(
                            _(u'The selected view requires a content object')))
                    elif not view.is_instance_view:
                        # if not an instance it does not need a content object
                        if data['object_id'] is not None:
                            data['object_id'] = None

        return super(RegionViewInlineForm, self).clean()

    class Meta:
        model = RegionView


class AuthorAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AuthorAdminForm, self).__init__(*args, **kwargs)
        self.fields['content_types'].choices = site.get_base_ctype_choices()


from registration.forms import RegistrationFormUniqueEmail
from captcha.fields import CaptchaField
from cyclope.utils import CrispyFormsSimpleMixin

class RegistrationFormWithCaptcha(RegistrationFormUniqueEmail,
                                    CrispyFormsSimpleMixin):
    captcha = CaptchaField(label=_("Security code"))
