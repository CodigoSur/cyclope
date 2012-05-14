#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010 Código Sur - Nuestra América Asoc. Civil / Fundación Pacificar.
# All rights reserved.
#
# This file is part of Cyclope.
#
# Cyclope is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Cyclope is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
models
------
"""
from datetime import datetime
import os

from django.db import models
from django.db.models import get_model
from django.utils.translation import ugettext_lazy as _
from django.contrib.comments import Comment
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist, ImproperlyConfigured
from django.conf import settings
from django.contrib.admin.models import LogEntry
from django.db.models.signals import post_save, pre_delete

from rosetta.poutil import find_pos
from tagging_autocomplete.models import TagAutocompleteField
import mptt
from autoslug.fields import AutoSlugField
from filebrowser.fields import FileBrowseField
from jsonfield import JSONField

from registration import signals as registration_signals

import cyclope
from cyclope.core.collections.models import Collection

# we add South introspection rules for custom field TagAutocompleteField
# this shouldn't be necessary once South incorporates this rule
from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^tagging_autocomplete\.models\.TagAutocompleteField"])


class SiteSettings(models.Model):
    """Model to store site-wide settings.

    Updating SiteSettings will update related cyclope.settings values.
    """
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
    newsletter_collection = models.ForeignKey(Collection, blank=True, null=True,
                                              verbose_name =_('newsletter collection'),
                                              help_text=_('This is the collection that will group the contents for your newsletters.'))
    rss_content_types = models.ManyToManyField(ContentType,
                                               verbose_name=_('whole feed contents'),
                                               help_text=_('contents to show in the whole feed'))

    def save(self, *args, **kwargs):
        self.id = 1
        super(SiteSettings, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    def __unicode__(self):
        return self.site.name

    class Meta:
        verbose_name = _('site settings')
        verbose_name_plural = _('site settings')


class Menu(models.Model):
    """Model for site menus.

    Only one Menu can be set to main_menu == True. If another is set to main,
    the previous main menu will be updated to main_menu == False.
    """
    name = models.CharField(_('name'), max_length=50, db_index=True, unique=True)
    slug = AutoSlugField(populate_from='name', always_update=True)
    main_menu = models.BooleanField(_('main menu'), default=False)

    def save(self, **kwargs):
        # set main_menu to False on previous main menu if main_menu is True
        if self.main_menu:
            try:
                old_main = self.__class__.objects.get(main_menu=True)
                old_main.main_menu = False
                old_main.save()
            except ObjectDoesNotExist:
                pass
        super(Menu, self).save(**kwargs)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('menu')
        verbose_name_plural = _('menus')


class MenuItem(models.Model):
    """Items for a Menu.

    Items always belong to one menu and they can be ordered in a tree structure.
    """
    menu = models.ForeignKey(Menu, verbose_name=_('menu'),
                             db_index=True, related_name='menu_items')
    name = models.CharField(_('name'), max_length=50, db_index=True)
    parent = models.ForeignKey('self', verbose_name=_('parent'),
                              related_name=_('children'),
                              null=True, blank=True)
    slug = AutoSlugField(populate_from='name', unique_with=('parent'),
                         always_update=True)
    site_home = models.BooleanField(_('site home'), default=False)
    custom_url = models.CharField(_('custom URL'), max_length=200,
                                  blank=True, default='')
    url = models.CharField(editable=False, max_length=255, unique=True, db_index=True)
    active = models.BooleanField(default=True, db_index=True)
    layout = models.ForeignKey('Layout', verbose_name=_('layout'),
                               null=True, blank=True)
    persistent_layout =  models.BooleanField(_('Persistent layout'), default=False,
                                      help_text=_('If the layout is marked as persistent it will be in use until the user navigates to a menu item which explicitly specifies a different Layout'))


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

    view_options = JSONField(default="{}") # default is taken from ViewOptionsForm

    def save(self, **kwargs):
        #TODO(nicoechaniz): Review this method
        # check that data is consistent
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

        if self.site_home:
            old_home = MenuItem.objects.filter(site_home=True)
            for item in old_home:
                item.site_home = False
                item.save()

        # If this is not a new MenuItem and the Menu is changed, we "move" all
        # the childrens to the new Menu.
        if self.pk is not None:
            old_menu_item = MenuItem.objects.get(pk=self.pk)
            if old_menu_item.menu != self.menu:
                for child in self.get_descendants():
                    child.menu = self.menu
                    child.save()

        # We have to save, to be able to generate an url
        super(MenuItem, self).save()

        if self.custom_url:
            self.url = self.custom_url
        else:
            self.url = "/".join([a.slug for a in self.get_ancestors()]+[self.slug])

        super(MenuItem, self).save(**kwargs)

    def get_layout(self):
        if self.layout:
            layout = self.layout
        else:
            layout = cyclope.settings.CYCLOPE_DEFAULT_LAYOUT
        return layout

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('menu item')
        verbose_name_plural = _('menu items')

try:
    mptt.register(MenuItem)
except mptt.AlreadyRegistered:
    pass

class RegionView(models.Model):
    """Holds configuration data for a frontend view to be displayed in a region of a particular Layout.
    """
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
    view_options = JSONField(default="{}") # default is taken from ViewOptionsForm

    def __unicode__(self):
        return '%s/%s' % (self.content_type.model, self.content_view)


class Layout(models.Model):
    """Given a theme template, a Layout configures which frontend views will be displayed in each region.
    """
    name = models.CharField(_('name'), max_length=50,
                            db_index=True, unique=True)
    slug = AutoSlugField(populate_from='name', db_index=True,
                         always_update=True)
    # template choices are set in the form
    template = models.CharField(_('layout template'), max_length=100)

    def __unicode__(self):
        return self.name

    def get_template_path(self):
        theme = cyclope.settings.CYCLOPE_CURRENT_THEME
        return 'cyclope/themes/%s/%s' % (theme, self.template)

    class Meta:
        verbose_name = _('layout')
        verbose_name_plural = _('layouts')


class RelatedContent(models.Model):
    """Relation between BaseContent derived models."""

    self_type = models.ForeignKey(ContentType, db_index=True,
                                     verbose_name=_('content type'),
                                     related_name='related_contents_lt')
    self_id = models.PositiveIntegerField(db_index=True)

    other_type = models.ForeignKey(ContentType, db_index=True,
                                     verbose_name=_('content type'),
                                     related_name='related_contents_rt')
    other_id = models.PositiveIntegerField(db_index=True)

    self_object = generic.GenericForeignKey(ct_field='self_type',
                                                  fk_field='self_id')
    other_object = generic.GenericForeignKey(ct_field='other_type',
                                                  fk_field='other_id')

    order = models.IntegerField(blank = True, null = True, db_index=True)

    def __unicode__(self):
        return self.other_object.name

    class Meta:
        verbose_name = _('related content')
        verbose_name_plural = _('related contents')
        ordering = ['order', ]


class BaseContent(models.Model):
    """Parent class for every content model.
    """
    name = models.CharField(_('name'), max_length=250,
                             db_index=True, blank=False)
    slug = AutoSlugField(populate_from='name', unique=True,
                         db_index=True, always_update=True)
    tags = TagAutocompleteField(_('tags'))
    published =  models.BooleanField(_('published'), default=True)
    related_contents = generic.GenericRelation(RelatedContent,
                                               object_id_field='self_id',
                                               content_type_field='self_type')
    creation_date = models.DateTimeField(_('creation date'),
                                         editable=True, default=datetime.now())
    modification_date = models.DateTimeField(_('modification date'), auto_now=True,
                                             editable=False, default=datetime.now())
    allow_comments = models.CharField(_('allow comments'), max_length=4,
                                choices = (
                                    ('SITE',_('default')),
                                    ('YES',_('enabled')),
                                    ('NO',_('disabled'))
                                ), default='SITE')
    comments = generic.GenericRelation(Comment, object_id_field="object_pk")

    def get_absolute_url(self):
        return '/%s/%s/' % (self._meta.object_name.lower(), self.slug)

    @classmethod
    def get_app_label(cls):
        return cls._meta.app_label

    @classmethod
    def get_object_name(cls):
        return cls._meta.object_name.lower()

    @classmethod
    def get_verbose_name(cls):
        return cls._meta.verbose_name

    @property
    def get_last_change_date(self):
        entries = LogEntry.objects.filter(
            content_type=ContentType.objects.get_for_model(self).id,
            object_id=self.pk)

        if entries:
            last = entries.latest('action_time')
            return last.action_time


    def translations(self):
        trans_links = []

        for lang in settings.LANGUAGES:
            # we look for the number rosetta uses to identity an app
            # which can be different for each language
            lang_code = lang[0]
            app_idx = None
            for i, path in enumerate(find_pos(lang_code)):
                project_path = cyclope.settings.CYCLOPE_PROJECT_PATH
                common_prefix = os.path.commonprefix([path, project_path])
                if common_prefix == project_path:
                    # we found the position for our app
                    app_idx = i
                    break
            if app_idx is not None:
                signature = "%s/%s/%s/" % (self._meta.app_label,
                                       self._meta.module_name, self.slug)
                trans_links.append(
                    u'<a href="/rosetta/select/%s/%s/?query=%s">%s</a> '
                    % (lang[0], app_idx, signature, _(lang[1])))
        trans_links = ''.join(trans_links)
        return trans_links

    translations.allow_tags = True
    translations.short_description = _('translations')

    def __unicode__(self):
        return self.name

    class Meta:
        abstract = True


class Author(models.Model):
    """Model to be used for every content that needs an author.

    This referes to the author of the content, not to the user uploading it.
    """
    name = models.CharField(_('name'), max_length=250,
                             db_index=True, blank=False)
    slug = AutoSlugField(populate_from='name', unique=True,
                         db_index=True, always_update=True)
    image = FileBrowseField(_('image'), max_length=100, format='Image',
                            directory='author_images/',
                            blank=True, default='')
    origin = models.CharField(_('origin'), max_length=250, db_index=True,
                               blank=True, default='')
    notes = models.TextField(_('notes'), blank=True, default='')
    content_types = models.ManyToManyField(
        ContentType, db_index=True, verbose_name=_('content types'),
        help_text=_('Select the content types this author is related to.'),)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('author')
        verbose_name_plural = _('authors')


class Source(models.Model):
    name = models.CharField(_('name'),max_length=250,
                             db_index=True, blank=False, unique=True)
    slug = AutoSlugField(populate_from='name', unique=True, db_index=True,
                         always_update=True)
    link = models.CharField(_('link'), max_length=250, blank=True, default='')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('source')
        verbose_name_plural = _('sources')

class Image(models.Model):
    """A simple image model.
    """
    image =  FileBrowseField(_('image'), max_length=100, format='Image',
                             directory='pictures/')

    def thumbnail(self):
        return '<img src="%s"/>' % self.image.url_thumbnail

    thumbnail.short_description = _('Thumbnail Image')
    thumbnail.allow_tags = True

    class Meta:
        verbose_name = _('image')
        verbose_name_plural = _('images')


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)

    avatar = models.ImageField(_('avatar'), max_length=100,
                               blank=True, upload_to="uploads/avatars/")
    city = models.CharField(_('city'), max_length=100, blank=True)
    about = models.TextField(_('about myself'), max_length=1000, blank=True)

    public = models.BooleanField(
        _('public'), default=True,
        help_text=_('Choose whether your profile info should be publicly visible or not'))

    def get_absolute_url(self):
        return ('profiles_profile_detail', (), { 'username': self.user.username })
    get_absolute_url = models.permalink(get_absolute_url)


# Signal callbacks

def _create_profile_upon_activation(*args, **kwargs):
    UserProfile.objects.create(user=kwargs['user'])

registration_signals.user_activated.connect(_create_profile_upon_activation)

def _delete_related_contents(sender, instance, **kwargs):
    # cascade delete does not delete the RelatedContent elements
    # where this object is the related content, so we do it here.
    # (this deletes the relation, not the object)
    ctype = ContentType.objects.get_for_model(sender)
    if hasattr(instance, 'id'):
        related_from = RelatedContent.objects.filter(other_type=ctype,
                                                    other_id=instance.id)
        for obj in related_from:
            obj.delete()

pre_delete.connect(_delete_related_contents)

