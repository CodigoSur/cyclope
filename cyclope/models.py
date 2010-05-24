# *-- coding:utf-8 --*
"""
models
------
"""

from django.db import models
from django.db.models import get_model
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist, ImproperlyConfigured

from tagging_autocomplete.models import TagAutocompleteField
from imagekit.models import ImageModel

import mptt
from autoslug.fields import AutoSlugField
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
    name = models.CharField(_('name'), max_length=50, db_index=True, unique=True)
    slug = AutoSlugField(populate_from='name', always_update=True)
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
# maybe we should try django-polymorphic and see how MPTT behaves
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

    content_type = models.ForeignKey(ContentType,
                     verbose_name=_('type'), related_name='menu_entries',
                     blank=True, null=True)
    object_id = models.PositiveIntegerField(_('object'),
        db_index=True, blank=True, null=True)
    content_object = generic.GenericForeignKey(
        'content_type', 'object_id')

    # content_view choices are set through an AJAX view
    content_view = models.CharField(_('view'), max_length=255,
                                    blank=True, default='')

    def save(self):
        # check that data is consistent
        #TODO(nicoechaniz): raise appropriate exceptions
        # a content object without a content type is invalid so we unset it
        if self.object_id and not self.content_type:
            self.object_id = None
        # a content view without a content type is invalid so we unset it
        if self.content_view != '' and not self.content_type:
            self.content_view = ''
        # get the default view for the content_type if no view is selected
        if self.content_type and self.content_view == '':
            model = get_model(self.content_type.app_label,
                              self.content_type.model)
            self.content_view = cyclope.core.frontend.site.get_default_view_name(model)

        if self.custom_url:
            self.url = self.custom_url
        else:
            # when the item is being created, slug is populated on save,
            # so we generate it manualy in order to set the URL.
            if not self.slug:
                slug_field = self._meta.get_field_by_name('slug')[0]
                populate_value = getattr(self, slug_field.populate_from)
                self.slug = slug_field.slugify(populate_value)
            self.url = "/".join([a.slug for a in self.get_ancestors()]+[self.slug])

        super(MenuItem, self).save()

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
    tags = TagAutocompleteField(_('tags'))
    published =  models.BooleanField(_('published'), default=True)


    def get_instance_url(self, view_name):
        #TODO(nicoechaniz): this seems like a bad name. it returns the URL for an instance and for a non-instance as well.
        view = cyclope.core.frontend.site.get_view(self.__class__, view_name)
        if view.is_instance_view:
            return '%s/%s/%s/View/%s'\
                    % (self._meta.app_label,
                       self._meta.object_name.lower(),
                       self.slug, view_name)
        else:
            return '%s/%s/View/%s'\
                    % (self._meta.app_label,
                       self._meta.object_name.lower(), view_name)

    def get_absolute_url(self):
        view_name = cyclope.core.frontend.site.get_default_view_name(self.__class__)
        return "/"+ self.get_instance_url(view_name)

    @classmethod
    def get_model_url(cls, view_name):
        return '%s/%s/View/%s'\
                % (cls._meta.app_label, cls._meta.object_name.lower(), view_name)

    def __unicode__(self):
        return self.name

    class Meta:
        abstract = True


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


class Picture(ImageModel, BaseContent):
    original_image = models.ImageField(_('image'), upload_to='uploads/images')
    num_views = models.PositiveIntegerField(editable=False, default=0)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()

    class IKOptions:
        # This inner class is where we define the ImageKit options for the model
        spec_module = 'cyclope.imagekit_default_specs'
        cache_dir = 'image_cache'
        image_field = 'original_image'
        save_count_as = 'num_views'

    def thumbnail(self):
        return '<img src="%s"/>' % self.thumbnail_image.url

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('image')
        verbose_name_plural = _('images')

class RegionView(models.Model):
    region = models.CharField(_('region'), max_length=100,
                              blank=True, default='')
    layout = models.ForeignKey('Layout')
    content_type = models.ForeignKey(ContentType,
                     verbose_name=_('type'), related_name='region_views',
                     blank=True, null=True)
    content_view = models.CharField(_('view'), max_length=255,
                                    blank=True, default='')

    weight = models.PositiveIntegerField(verbose_name=_('weight'), default=0,
                                         blank=True, null=True)
    object_id = models.PositiveIntegerField(
        db_index=True, verbose_name=_('object'),
        blank=True, null=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    def __unicode__(self):
        return '%s/%s' % (self.content_type.model, self.content_view)
        #if self.content_type and self.content_view:
        #    return '%s/%s' % (self.content_type.model, self.content_view)
        #else:
        #    return self.region


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
