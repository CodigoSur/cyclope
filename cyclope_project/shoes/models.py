from django.db import models
from django.utils.translation import ugettext as _

from cyclope.models import BaseContent
from cyclope.core.collections.models import Collectible

class Color(BaseContent):
    pass

class Shoe(BaseContent, Collectible):
    cut = models.CharField(_('cut'), max_length=100, blank=True)
    material = models.CharField(_('material'), max_length=100, blank=True)
    sole = models.CharField(_('sole'), max_length=100, blank=True)
    colors = models.ManyToManyField(Color, blank=True, null=True)
    heel = models.CharField(_('heel'), max_length=10, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('shoe')
        verbose_name_plural = _('shoes')
