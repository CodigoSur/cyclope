
from django import forms
from django.conf import settings as django_settings
from django.utils.translation import ugettext as _
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db.models import get_model

from mptt.forms import TreeNodeChoiceField

from cyclope.widgets import WYMEditor
from cyclope.models import StaticPage, MenuItem, SiteSettings, Layout, RegionView
import cyclope.settings as cyc_settings
from cyclope import site as cyc_site

class AjaxChoiceField(forms.ChoiceField):
    """
    ChoiceField that always returns true for validate()
    """
    # we always return true because we don't know what choices were available
    # at submit time, because they were populated through AJAX.
    #ToDo: see if there's a way to find out which choices are valid.
    def validate(self, value):
        return True

def populate_type_choices(myform):
    ctype_choices = [('', '------')]
    for model in cyc_site._registry:
        ctype = ContentType.objects.get_for_model(model)
        ctype_choices.append((ctype.id, ctype.name))
    myform.fields['content_type'].choices = ctype_choices



class BaseContentAdminForm(forms.ModelForm):
    menu_items = forms.ModelMultipleChoiceField(
                    queryset = MenuItem.tree.all(), required=False,
                    )

    def __init__(self, *args, **kwargs):
        super(BaseContentAdminForm, self).__init__(*args, **kwargs)
        if self.instance.id is not None:
            selected_items = [ values[0] for values in MenuItem.objects.filter(
                content_object__id=self.instance.id).values_list('id') ]
            self.fields['menu_items'].initial = selected_items


class StaticPageAdminForm(BaseContentAdminForm):
    summary = forms.CharField(widget=WYMEditor())
    text = forms.CharField(widget=WYMEditor())

    class Meta:
        model = StaticPage


class MenuItemAdminForm(forms.ModelForm):
    # content_view choices get populated through javascript when a template is selected
    content_view = AjaxChoiceField(required=False)
    parent = TreeNodeChoiceField(queryset=MenuItem.tree.all(), required=False)

    def __init__(self, *args, **kwargs):
        super(MenuItemAdminForm, self).__init__(*args, **kwargs)
        if self.instance.id is not None:
            # chainedSelect will show the selected choice
            # if it is present before filling the choices through AJAX
            selected_view = MenuItem.objects.get(id=self.instance.id).content_view
            self.fields['content_view'].choices = [(selected_view, selected_view)]
        populate_type_choices(self)

    def clean(self):
        #ToDo: data consistency is being done at model level see models.MenuItem.save(). Implement form validation.
        obj = self.instance
        if obj.custom_url and \
        (obj.content_type or obj.content_object or obj.content_view):
            raise ValidationError(
                _(u'You can not set a Custom URL for menu entries \
                    with associated content'))
        return super(MenuItemAdminForm, self).clean()

    class Meta:
        model = MenuItem

    class Media:
        js = (
             cyc_settings.CYCLOPE_MEDIA_URL +"js/jquery.chainedSelect.js",
             )

class SiteSettingsAdminForm(forms.ModelForm):
    theme = forms.ChoiceField(
        choices=[ (theme_name,
                  getattr(cyc_settings.CYCLOPE_THEMES, theme_name).verbose_name)
                  for theme_name in cyc_settings.CYCLOPE_THEMES.available ],
        required=True)

    class Meta:
        model = SiteSettings


class LayoutAdminForm(forms.ModelForm):
    template = forms.ChoiceField(required=True)

    def __init__(self, *args, **kwargs):
        super(LayoutAdminForm, self).__init__(*args, **kwargs)
        from cyclope.utils import themes

        # We are asuming there's only one site but this should be modified
        # if we start using the sites framework and make cyclope multi-site.
        #ToDo: adapt for multi-site
        try:
            theme_name = SiteSettings.objects.get().theme
        except:
            return
        theme_settings = getattr(cyc_settings.CYCLOPE_THEMES, theme_name)
        tpl_choices = [(tpl, tpl_settings['verbose_name'])
                       for tpl, tpl_settings
                       in theme_settings.layout_templates.items()]

        self.fields['template'].choices = tpl_choices

    class Meta:
        model = Layout


class RegionViewInlineForm(forms.ModelForm):

    # Region choices get populated through javascript
    # when a template is selected.
    # The corresponding json view is CyclopeSite.layout_regions_json()
    region = AjaxChoiceField(required=False)
    content_view = AjaxChoiceField(required=False)

    def __init__(self, *args, **kwargs):
        super(RegionViewInlineForm, self).__init__(*args, **kwargs)
        if self.instance.id is not None:
            # chainedSelect will show the selected choice
            # if it is present before filling the choices through AJAX
            # so we set them here at __init__ time
            obj = RegionView.objects.get(id=self.instance.id)
            if obj.region:
                selected_region = obj.region
                self.fields['region'].choices = [(selected_region,
                                                  selected_region)]
            if obj.content_view:
                selected_view = obj.content_view
                self.fields['content_view'].choices = [(selected_view,
                                                        selected_view)]
        populate_type_choices(self)

    def clean(self):
        obj = self.instance
        if not obj.content_type:
            raise(ValidationError(_(u'Content type can not be empty')))
        if obj.content_object:
            try:
                getattr(obj.content_object, obj.content_type.model)
            except:
                raise(ValidationError(
                    _(u'Content object does not match content type')))
        if obj.content_type:
            if (obj.content_view == '' or not obj.content_view):
                raise(ValidationError(
                    _(u'You need to select a content view')))
            if not obj.region:
                raise(ValidationError(_(u'You need to select a region')))

        return super(RegionViewInlineForm, self).clean()


    class Media:
        js = (
             cyc_settings.CYCLOPE_MEDIA_URL +"js/jquery.chainedSelect.js",
             )

    class Meta:
        model = RegionView
