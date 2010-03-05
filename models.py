# *-- coding:utf-8 --*

from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
import mptt
from autoslug.fields import AutoSlugField

import site as cyc_site

from cyclope.core.collections.models import Collectible

#class SiteSettings(models.Model):
#    name = models.CharField(_('domain'),max_length=250,
#                                 db_index=True, blank=False, unique=True)
#
#    slug = AutoSlugField(populate_from='name')
##    theme = models.CharField(_('templating theme'), max_length=250)
#    comments = models.CharField(_('allow comments'), max_length=4,
#                                choices = (
#                                    ('YES',_('enabled')),
#                                    ('NO',_('disabled'))
#                                ))
#
#    global_title = models.CharField(_('global title'), max_length=250, blank=True, default='')
#    keywords = models.TextField(_('keywords'), blank=True, default='')
#    description = models.TextField(_('description'), blank=True, default='')
#
#    def __unicode__(self):
#        return self.name


class Menu(models.Model):
    name = models.CharField(_('name'), max_length=50, db_index=True)
    def __unicode__(self):
        return self.name


class MenuItem(models.Model):
# this class could inherit from Category but mptt does not support it.
    menu = models.ForeignKey(Menu, verbose_name=_('menu'), db_index=True)
    name = models.CharField(_('name'), max_length=50, db_index=True)
    parent = models.ForeignKey('self', verbose_name=_('parent'),
                               related_name=_('children'), null=True, blank=True)
#    slug = AutoSlugField(populate_from='name', unique_with='parent')
    custom_url = models.URLField(_('custom URL'), blank=True) #help=_('If set, overides other settings'))
    url = models.URLField(editable=False)
    active = models.BooleanField(default=True)

    content_type = models.ForeignKey(ContentType,
                     verbose_name=_('type'), related_name='menu_entries', blank=True, null=True)
    content_object = models.ForeignKey('BaseContent',
                     verbose_name=_('object'), related_name='menu_entries', blank=True, null=True)

    content_view = models.CharField(_('view'), max_length=255, blank=True, null=True, choices=(('',''),))
    # content_view choices ar overriden by the form definition


    def save(self):
        #if self.content_view:
        #    self.url = self.content_view

        super(MenuItem, self).save()

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('menu item')
        verbose_name_plural = _('menu items')

mptt.register(MenuItem)


class BaseContent(models.Model):
    """
    Base model for content elements.
    """
    name = models.CharField(_('name'), max_length=250,
                             db_index=True, blank=False)
    slug = AutoSlugField(populate_from='name', unique=True, db_index=True)


    def get_instance_url(self):
        return '%s/%s/%s' % (self._meta.app_label,
                             self._meta.object_name.lower(), self.slug)

    @classmethod
    def get_url_pattern(cls):
        return '%s/%s/(?P<slug>.*)'\
                % (cls._meta.app_label, cls._meta.object_name.lower())

    @classmethod
    def get_view_params(cls):
        return {'queryset': cls.objects,
                'template_object_name': cls._meta.object_name.lower()}

    def __unicode__(self):
        return self.name


class BaseCommentedContent(BaseContent):
    allow_comments = models.CharField(_('allow comments'), max_length=4,
                                choices = (
                                    ('SITE',_('default')),
                                    ('YES',_('enabled')),
                                    ('NO',_('disabled'))
                                ), default='SITE')

    class Meta:
        abstract = True


# should this be moved to it's own app? should we just use flatpages?
class StaticPage(BaseCommentedContent, Collectible):
    #menuitem = models.ForeignKey(MenuItem, verbose_name=_('menu item'),
    #                             blank=True, null=True)
    summary = models.TextField(_('summary'), blank=True)
    text = models.TextField(_('text'))

    def __unicode__(self):
        return self.name


class LayoutRegion(models.Model):
    layout = models.ForeignKey('Layout')
    block_view = models.ForeignKey('BlockView')
    # region choices must be set from settings.CYCLOPE_LAYOUT_TEMPLATES[''][1]
    region = models.CharField(_('region'), max_length=100, choices=(('Left Sidebar','left'),))

    def __unicode__(self):
        return ''


class Layout(models.Model):
    name = models.CharField(_('name'), max_length=50, db_index=True)
    # template choices must be set from settings.CYCLOPE_LAYOUT_TEMPLATES
    # CYCLOPE_LAYOUT_TEMPLATES = {_('base_layout'):
    #                             ('base_layout.html',
    #                             ('header', 'left_sidebar', 'content', 'footer')}
    template = models.CharField(_('layout template'),
                   max_length=100, choices=(('Base Layout','base_layout.html'),))
    blocks = models.ManyToManyField('BlockView', through=LayoutRegion)

    def __unicode__(self):
        return self.name


class BlockView(models.Model):
    # view choices must be set from site._registry
    view = models.CharField(_('layout template'),
                   max_length=100, choices=(('news_article_detail','news_article_detail'),))

    def __unicode__(self):
        return self.view
