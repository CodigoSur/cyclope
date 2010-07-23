# -*- coding: utf-8 -*-

from django.contrib import admin
from django import forms

from django.utils.translation import ugettext_lazy as _

from cyclope.core.collections.admin import CollectibleAdmin
from cyclope.admin import BaseContentAdmin
from cyclope.forms import BaseContentAdminForm
from cyclope.widgets import WYMEditor

from models import StaticPage

class StaticPageAdminForm(BaseContentAdminForm):
#    text = forms.CharField(label=_('Text'), widget=WYMEditor())

    class Meta:
        model = StaticPage

class StaticPageAdmin(CollectibleAdmin, BaseContentAdmin):
    form = StaticPageAdminForm

admin.site.register(StaticPage, StaticPageAdmin)
