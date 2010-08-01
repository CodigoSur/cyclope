# -*- coding: utf-8 -*-

from django.contrib import admin
from cyclope.core.collections.admin import CollectibleAdmin
from cyclope.admin import BaseContentAdmin
from cyclope.forms import BaseContentAdminForm

from models import *

from django.forms import ModelForm


class ShoeForm(BaseContentAdminForm):
    class Meta:
        model = Shoe

class ShoeAdmin(CollectibleAdmin, BaseContentAdmin):
    form = ShoeForm
    list_filter = CollectibleAdmin.list_filter
    #search_fields = ('name', 'pretitle', 'color', 'material', )


admin.site.register(Shoe, ShoeAdmin)
admin.site.register(Color)
