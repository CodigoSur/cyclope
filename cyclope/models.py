# *-- coding:utf-8 --*
"""Django models"""

from django.db import models
from django.db.models import get_model
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist

import mptt
from autoslug.fields import AutoSlugField

from cyclope.core.collections.models import Collectible
import cyclope

class SiteSettings(models.Model):
    site = models.ForeignKey(Site, unique=True)
    theme = models.CharField(_('templating theme'), max_length=250)
    default_layout = models.ForeignKey('Layout',
                                       verbose_name=_('default layout'),
                                       null=True, blank=True)
    allow_comments = models.CharField(_('allow comments'), max_length=4,
                                      choices = (
                                                 ('YES',_('enabled')),
                                                 ('NO',_('disabled'))
                                    ))

    global_title = models.CharField(_('global title'),
                                    max_length=250, blank=True, default='')
    keywords = models.TextField(_('keywords'), blank=True, default='')
    description = models.TextField(_('description'), blank=True, default='')

    def __unicode__(self):
        return self.site.name

    class Meta:
        verbose_name = _('site settings')
        verbose_name_plural = _('site settings')


class Menu(models.Model):
    name = models.CharField(_('name'), max_length=50, db_index=True)
    main_menu = models.BooleanField(_('main menu'), default=False)

    def save(self):
        # set main_menu to False on previous main menu if main_menu is True
        if self.main_menu:
            try:
                old_main = self.__class__.objects.get(main_menu=True)
                old_main.main_menu = False
                old_main.save()
            except ObjectDoesNotExist:
                pass
        super(Menu, self).save()

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('menu')
        verbose_name_plural = _('menus')


class MenuItem(models.Model):
# this class could inherit from Category
# but mptt does not support inheritance well
# maybe we should try django-polymorphic or change MPTT for Treebeard
    menu = models.ForeignKey(Menu, verbose_name=_('menu'),
                             db_index=True, related_name='menu_items')
    name = models.CharField(_('name'), max_length=50, db_index=True)
    parent = models.ForeignKey('self', verbose_name=_('parent'),
                              related_name=_('children'),
                              null=True, blank=True)
    slug = AutoSlugField(populate_from='name', unique_with='parent',
                         always_update=True)
    site_home = models.BooleanField(_('site home'), default=False)
    custom_url = models.CharField(_('custom URL'), max_length=200,
                                  blank=True, default='',
                                  help_text=_(
                                    u"Either set an URL here or \
                                    select a content type and view."))
    url = models.CharField(editable=False, max_length=255, unique=True, db_index=True)
    active = models.BooleanField(default=True, db_index=True)
    layout = models.ForeignKey('Layout', verbose_name=_('layout'),
                               null=True, blank=True)
    content_type = models.ForeignKey(ContentType, verbose_name=_('type'),
                                     related_name='menu_entries',
                                     blank=True, null=True)
    content_object = models.ForeignKey('BaseContent',
                     verbose_name=_('object'), related_name='menu_entries',
                     blank=True, null=True)
    # content_view choices are set through an AJAX view
    content_view = models.CharField(_('view'), max_length=255,
                                    blank=True, default='')

    def save(self):
        # check that data is consistent
        #ToDo: raise appropriate exceptions
        if self.content_object and not self.content_type:
            self.content_type = ContentType.objects.get_for_model(
                self.content_object)
        if self.content_view != '' and not self.content_type:
            raise Exception(_(u'No content selected'))

        if self.content_object:
            try:
                getattr(self.content_object, self.content_type.model)
            except:
                raise Exception(
                    _(u'%s: "%s" does not exist' % \
                      (self.content_type.model, self.content_object)))

        if self.content_type and self.content_view == '':
            model = get_model(self.content_type.app_label,
                              self.content_type.model)
            self.content_view = cyclope.core.frontend.site.get_default_view_name(model)

        if not self.content_type and not self.custom_url:
            self.active = False
        if self.site_home:
            try:
                old_home_item = self.__class__.objects.get(site_home=True)
                old_home_item.site_home = False
                old_home_item.save()
            except ObjectDoesNotExist:
                pass
            finally:
                self.url = ""
        else:
            self.url = self.get_content_url()
        super(MenuItem, self).save()

    def get_content_url(self):
        if self.custom_url:
            return self.custom_url
        else:
            model = get_model(self.content_type.app_label,
                              self.content_type.model)
            if self.content_object:
                obj = model.objects.get(pk=self.content_object.pk)
                return obj.get_absolute_url(self.content_view)
            else:
                return model.get_model_url(self.content_view)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('menu item')
        verbose_name_plural = _('menu items')

mptt.register(MenuItem)


class BaseContent(models.Model):
    """
    Parent class for every content model.
    """
    name = models.CharField(_('name'), max_length=250,
                             db_index=True, blank=False)
    slug = AutoSlugField(populate_from='name', unique=True,
                         db_index=True, always_update=True)

    def get_absolute_url(self, view_name):
        return '%s/%s/%s/View/%s'\
                % (self._meta.app_label,
                   self._meta.object_name.lower(),
                   self.slug, view_name)
    #@classmethod
    #def get_url_pattern(cls, view):
    #    view_name = view.name
    #    is_instance_view = view.is_instance_view
    #    if is_instanceview:
    #        return '%s/%s/(?P<slug>.*)/View/%s'\
    #                % (cls._meta.app_label,
    #                   cls._meta.object_name.lower(), view_name)
    #    else:
    #        return '%s/%s/View/%s'\
    #                % (cls._meta.app_label,
    #                   cls._meta.object_name.lower(), view_name)

    @classmethod
    def get_model_url(cls, view):
        return '%s/%s/View/%s'\
                % (cls._meta.app_label, cls._meta.object_name.lower(), view)

    @classmethod
    def default_detail_params(cls):
        return {'queryset': cls.objects,
                'template_object_name': cls._meta.object_name.lower()}

    def __unicode__(self):
        return self.name


class BaseCommentedContent(BaseContent):
    """Parent class for content objects that can have comments."""
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
    summary = models.TextField(_('summary'), blank=True)
    text = models.TextField(_('text'))

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('static page')
        verbose_name_plural = _('static pages')


class RegionView(models.Model):
    layout = models.ForeignKey('Layout')
    content_type = models.ForeignKey(ContentType,
                     verbose_name=_('type'), related_name='region_views',
                     blank=True, null=True)
    content_object = models.ForeignKey('BaseContent',
                     verbose_name=_('object'), related_name='region_views',
                     blank=True, null=True)
    content_view = models.CharField(_('view'), max_length=255,
                                    blank=True, default='')
    region = models.CharField(_('region'), max_length=100,
                              blank=True, default='')
    weight = models.PositiveIntegerField(verbose_name=_('weight'), default=0,
                                         blank=True, null=True)

    def __unicode__(self):
        return '%s/%s' % (self.content_type.model, self.content_view)


class Layout(models.Model):
    name = models.CharField(_('name'), max_length=50,
                            db_index=True, unique=True)
    slug = AutoSlugField(populate_from='name', db_index=True,
                         always_update=True)
    # template choices are set in the form
    template = models.CharField(_('layout template'), max_length=100)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('layout')
        verbose_name_plural = _('layouts')
