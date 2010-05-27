# *-- coding:utf-8 --*
"""
apps.articles.models
--------------------
"""

from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from autoslug.fields import AutoSlugField
from cyclope.core.collections.models import Collectible
from cyclope.models import BaseContent
from cyclope.apps.medialibrary.models import Picture

YES_NO = (('YES', _('yes')), ('NO', _('no')),)

class Author(models.Model):
    name = models.CharField(_('name'),max_length=250,
                             db_index=True, blank=False, unique=True)
    slug = AutoSlugField(populate_from='name', unique=True, db_index=True)
    country = models.CharField(max_length=250, db_index=True,
                               blank=True, default='')
    notes = models.TextField(_('notes'), blank=True, default='')
    def __unicode__(self):
        return self.name


class Source(models.Model):
    name = models.CharField(_('name'),max_length=250,
                             db_index=True, blank=False, unique=True)
    slug = AutoSlugField(populate_from='name', unique=True, db_index=True)

    link = models.CharField(_('link'), max_length=250, blank=True, default='')

    def __unicode__(self):
        return self.name


class Article(BaseContent, Collectible):
    pretitle = models.CharField(_('pre-title'), max_length=250, blank=True)
    summary = models.TextField(_('summary'))
    text = models.TextField(_('text'))
    author = models.ForeignKey(Author, verbose_name=_('author'))
    source = models.ForeignKey(Source, verbose_name=_('source'),
                               blank=True, null=True)
    creation_date = models.DateTimeField(_('creation date'),
                                     auto_now_add=True, editable=False)
    date = models.DateTimeField(_('date'), blank=True, null=True)
    pictures = models.ManyToManyField(Picture, null=True, blank=True,)

    allow_comments = models.CharField(_('allow comments'), max_length=4,
                                choices = (
                                    ('SITE',_('default')),
                                    ('YES',_('enabled')),
                                    ('NO',_('disabled'))
                                ), default='SITE')

    def first_picture(self):
        if self.pictures.count() > 0:
            return self.pictures.all()[0]

    class Meta:
        verbose_name = _('article')
        verbose_name_plural = _('articles')


class Attachment(models.Model):
    name = models.CharField(_('title'),max_length=250,
                             db_index=True, blank=False, unique=True)
    slug = AutoSlugField(populate_from='name', unique=True, db_index=True)
    article = models.ForeignKey(Article,
                                verbose_name=_('article'),
                                related_name=_('attachments'))
    description = models.CharField(_('description'), max_length=250,
                                   blank=True, db_index=True)
    file = models.FileField(_('file'), max_length=250, db_index=True,
                            upload_to='attachments')
    downloads = models.IntegerField(_('downloads'), default=0,
                                    blank=True, editable=False) #download counter

    def __unicode__(self):
        return '%s (%s)' % (self.name, self.file)
