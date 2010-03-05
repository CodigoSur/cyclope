
from django import forms
#from django.db.models import get_model
from mptt.forms import TreeNodeChoiceField

from cyclope.widgets import WYMEditor
from cyclope.models import StaticPage, MenuItem
from cyclope import site as cyc_site

#import site as cyc_site

class BaseContentAdminForm(forms.ModelForm):
    menu_items = forms.ModelMultipleChoiceField(
                    queryset = MenuItem.objects.all(),
                    required=False
                    )


class StaticPageAdminForm(BaseContentAdminForm):
#    text = forms.CharField(widget=WYMEditor())

    class Meta:
        model = StaticPage
#        model = get_model('cyclope', 'static_page')

class MenuItemAdminForm(forms.ModelForm):
    content_view = forms.ModelChoiceField(queryset=None, required=False)
    parent = TreeNodeChoiceField(queryset=MenuItem.tree.all(), required=False)

    def __init__(self, *args, **kwargs):
        super(MenuItemAdminForm, self).__init__(*args, **kwargs)
        choices = [('', '------')]

        if self.instance.pk is not None and self.instance.content_object:
            base_content = self.instance.content_object
            related = base_content._meta.get_all_related_objects()

            for obj in related:
                related_content_model = obj.model
                rel_name = related_content_model._meta.object_name.lower()
                try:
                    related_content = getattr(base_content, rel_name)
                    break
                except:
                    continue


            if related_content_model in cyc_site._registry:
                related_content_instance = related_content_model.objects.get(pk=self.instance.content_object.pk)

                for view_config in cyc_site._registry[obj.model]:
                    if view_config['default']:
                        url = related_content_instance.get_instance_url()
                    else:
                        url = '%s/%s' % (related_content_instance.get_instance_url(),
                                         view_config['view_name'])
                    choices.append((url, view_config['view_name']))

        else:
            pass
#        choices.sort(key=itemgetter(1))
        self.fields['content_view'].choices = choices

    class Meta:
        model = MenuItem
