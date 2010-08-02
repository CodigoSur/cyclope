# -*- coding: utf-8 -*-

from django.contrib import admin
from django import forms

from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType

from cyclope.core.collections.admin import CollectibleAdmin
from cyclope.widgets import WYMEditor
from cyclope.models import MenuItem
from cyclope import settings as cyc_settings
from models import StaticPage

class StaticPageAdminForm(forms.ModelForm):
    menu_items = forms.ModelMultipleChoiceField(label=_('Menu items'),
                    queryset = MenuItem.tree.all(), required=False,
                    )
    if cyc_settings.CYCLOPE_STATICPAGE_RICH_EDITOR:
        text = forms.CharField(label=_('Text'), widget=WYMEditor())

    def __init__(self, *args, **kwargs):
    # this was initially written to be used for any BaseContent, that's
    # why we don't assume the content_type to be pre-determined
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        if self.instance.id is not None:
            instance_type = ContentType.objects.get_for_model(self.instance)
            selected_items = [
                values[0] for values in
                MenuItem.objects.filter(
                    content_type=instance_type,
                    object_id=self.instance.id).values_list('id') ]
            self.fields['menu_items'].initial = selected_items

    class Meta:
        model = StaticPage


class StaticPageAdmin(CollectibleAdmin):
    # updates related menu_items information when a StaticPaget is saved
    form = StaticPageAdminForm

    def save_model(self, request, obj, form, change):
        super(CollectibleAdmin, self).save_model(request, obj, form, change)
        object_type = ContentType.objects.get_for_model(obj)
        selected_items_ids = form.data.getlist('menu_items')
        selected_items = set(MenuItem.objects.filter(pk__in=selected_items_ids))
        old_items = set(MenuItem.objects.filter(content_type=object_type,
                                                object_id=obj.id))
        discarded_items = old_items.difference(selected_items)
        new_items = selected_items.difference(old_items)
        for menu_item in discarded_items:
            menu_item.content_type = None
            menu_item.object_id = None
            menu_item.content_view = None
            menu_item.save()
        for menu_item in new_items:
            menu_item.content_type = object_type
            menu_item.object_id = obj.id
            menu_item.save()

admin.site.register(StaticPage, StaticPageAdmin)
