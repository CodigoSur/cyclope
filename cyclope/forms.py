# *-- coding:utf-8 --*
"""
forms
-----
"""

from django import forms
from django.conf import settings as django_settings
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.db.models import get_model
from django.contrib.contenttypes.models import ContentType

from mptt.forms import TreeNodeChoiceField

from cyclope.widgets import WYMEditor
from cyclope.models import MenuItem, BaseContent,\
                           SiteSettings, Layout, RegionView, UserProfile
from cyclope import settings as cyc_settings
from cyclope.core.frontend import site


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


class RelatedContentForm(forms.ModelForm):
    other_id= AjaxChoiceField(label=_('Content object'),)

    def __init__(self, *args, **kwargs):
        super(RelatedContentForm, self).__init__(*args, **kwargs)

        self.fields['other_type'].choices = site.get_base_ctype_choices()

        if self.instance.id is not None:
            content_object = self.instance.other_object
            self.fields['other_id'].choices = [(content_object.id,
                                                        content_object.name)]


class MenuItemAdminForm(forms.ModelForm):
    # content_view choices get populated through javascript
    # when a template is selected
    content_view = AjaxChoiceField(label=_('View'), required=False)
    object_id = AjaxChoiceField(label=_('Content object'), required=False)
    parent = TreeNodeChoiceField(label=_('Parent'), queryset=MenuItem.tree.all(), required=False)

    def __init__(self, *args, **kwargs):
        super(MenuItemAdminForm, self).__init__(*args, **kwargs)
        if self.instance.id is not None:
            # chainedSelect will show the selected choice
            # if it is present before filling the choices through AJAX
            menu_item = MenuItem.objects.get(id=self.instance.id)
            selected_view = menu_item.content_view
            self.fields['content_view'].choices = [(selected_view,
                                                    selected_view)]
            if menu_item.content_object:
                content_object = menu_item.content_object
                self.fields['object_id'].choices = [(content_object.id,
                                                        content_object.name)]
        self.fields['content_type'].choices = site.get_registry_ctype_choices()

    def clean(self):
        data = self.cleaned_data
        if data['object_id'] == '':
            data['object_id'] = None

        if data['custom_url'] and (data['content_type']
                                   or data['object_id']
                                   or data['content_view']):
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
                    if view.is_instance_view and data['object_id'] is None:
                        raise(ValidationError(
                            _(u'The selected view requires a content object')))
                    elif not view.is_instance_view:
                        # if not an instance it does not need a content object
                        if data['object_id'] is not None:
                            data['object_id'] = None

        return super(MenuItemAdminForm, self).clean()

    class Meta:
        model = MenuItem


class SiteSettingsAdminForm(forms.ModelForm):
    theme = forms.ChoiceField(label=_('Theme'),
        choices=[
            (theme_name,  getattr(cyc_settings.themes,
            theme_name).verbose_name)
            for theme_name in cyc_settings.themes.available ],
        required=True)

    class Meta:
        model = SiteSettings


class LayoutAdminForm(forms.ModelForm):
    template = forms.ChoiceField(label=_('Template'), required=True)

    def __init__(self, *args, **kwargs):
        super(LayoutAdminForm, self).__init__(*args, **kwargs)

        # We are asuming there's only one site but this should be modified
        # if we start using the sites framework and make cyclope multi-site.
        #TODO(nicoechaniz): adapt for multi-site
        try:
            theme_name = SiteSettings.objects.get().theme
        except:
            return
        theme_settings = getattr(cyc_settings.themes, theme_name)
        tpl_choices = [(tpl, tpl_settings['verbose_name'])
                       for tpl, tpl_settings
                       in theme_settings.layout_templates.items()]

        self.fields['template'].choices = tpl_choices

    class Meta:
        model = Layout


class RegionViewInlineForm(forms.ModelForm):

    # Choices for these fields get populated through javascript/JSON.
    region = AjaxChoiceField(label=_('Region'), required=False)
    content_view = AjaxChoiceField(label=_('View'), required=False)
    object_id = AjaxChoiceField(label=_('Content object'), required=False)

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
            if region_view.content_object:
                content_object = region_view.content_object
                self.fields['object_id'].choices = [(content_object.id,
                                                        content_object.name)]

        self.fields['content_type'].choices = site.get_registry_ctype_choices()

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
        self.fields['content_types'].choices = site.get_registry_ctype_choices()


from registration.forms import RegistrationFormUniqueEmail
from captcha.fields import CaptchaField

class RegistrationFormWithCaptcha(RegistrationFormUniqueEmail):
    captcha = CaptchaField(label=_("Security code"))


class UserProfileForm(forms.ModelForm):

    #def __init__(self, *args, **kwargs):
    #    super(UserProfileForm, self).__init__(*args, **kwargs)
    #    self.fields['avatar'].initial = ""

    def clean_avatar(self):
        from django.core.files.images import get_image_dimensions
        avatar = self.cleaned_data['avatar']
        w, h = get_image_dimensions(avatar)
        if w > 300 or h > 300:
            raise forms.ValidationError(_('Your avatar image is too big'))
        return avatar

    class Meta:
        model = UserProfile
        exclude = ('user',)
