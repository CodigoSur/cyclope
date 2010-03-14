
from django import forms
from django.conf import settings as django_settings
#from django.db.models import get_model
from mptt.forms import TreeNodeChoiceField

from cyclope.widgets import WYMEditor
from cyclope.models import StaticPage, MenuItem, SiteSettings, Layout, RegionView
from cyclope import site as cyc_site, settings as cyc_settings

class BaseContentAdminForm(forms.ModelForm):
    menu_items = forms.ModelMultipleChoiceField(
                    queryset = MenuItem.objects.all(),
                    required=False
                    )


class StaticPageAdminForm(BaseContentAdminForm):
    summary = forms.CharField(widget=WYMEditor())
    text = forms.CharField(widget=WYMEditor())

    class Meta:
        model = StaticPage
#        model = get_model('cyclope', 'static_page')

class MenuItemAdminForm(forms.ModelForm):
    # Choices get populated through javascript when a template is selected
    # the corresponding json view is CyclopeSite.layout_regions_json()

    content_view = forms.ChoiceField(required=False)
    parent = TreeNodeChoiceField(queryset=MenuItem.tree.all(), required=False)

    #def __init__(self, *args, **kwargs):
    #    super(MenuItemAdminForm, self).__init__(*args, **kwargs)
    #    choices = [('', '------')]
    #
    #    if self.instance.pk is not None and self.instance.content_object:
    #        base_content = self.instance.content_object
    #        related = base_content._meta.get_all_related_objects()
    #
    #        for obj in related:
    #            related_content_model = obj.model
    #            rel_name = related_content_model._meta.object_name.lower()
    #            try:
    #                related_content = getattr(base_content, rel_name)
    #                break
    #            except:
    #                continue
    #
    #        if related_content_model in cyc_site._registry:
    #            related_content_instance = related_content_model.objects.get(pk=self.instance.content_object.pk)
    #
    #            for view_config in cyc_site._registry[obj.model]:
    #                if view_config['is_default']:
    #                    url = related_content_instance.get_instance_url()
    #                else:
    #                    url = related_content_instance.get_instance_url(view_config['view_name'])
    #                choices.append((url, view_config['verbose_name']))
    #
    #    self.fields['content_view'].choices = choices

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
        from cyclope.utils import themes
        super(LayoutAdminForm, self).__init__(*args, **kwargs)

        # we are asuming there's only one site. but this should be modified
        # if we start using the sites framework and make cyclope multi-site
        theme_name = SiteSettings.objects.get().theme
        theme_settings = getattr(cyc_settings.CYCLOPE_THEMES, theme_name)

        tpl_choices = [(tpl, tpl_settings['verbose_name'])
                       for tpl, tpl_settings
                       in theme_settings.layout_templates.items()]

        self.fields['template'].choices = tpl_choices

    class Meta:
        model = Layout

class RegionViewInlineForm(forms.ModelForm):

    # Choices get populated through javascript when a template is selected
    # the corresponding json view is CyclopeSite.layout_regions_json()
    region = forms.ChoiceField(required=False)

    class Media:
        js = (
             cyc_settings.CYCLOPE_MEDIA_URL +"js/jquery.chainedSelect.js",
             )

    class Meta:
        model = RegionView
