# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from cyclope.models import BaseContent
from cyclope.core.collections.models import Collectible

class StaticPage(BaseContent, Collectible):
    summary = models.TextField(_('summary'), blank=True)
    text = models.TextField(_('text'))

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('static page')
        verbose_name_plural = _('static pages')
