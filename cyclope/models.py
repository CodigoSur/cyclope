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
import mptt
from autoslug.fields import AutoSlugField
from filebrowser.fields import FileBrowseField

import cyclope

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
                                  blank=True, default='',
                                  help_text=_(
                                    u"Either set an URL here or \
                                    select a content type and view."))
    url = models.CharField(editable=False, max_length=255, unique=True, db_index=True)
#    open_in_new_window = models.BooleanField(default=False)
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

        if self.site_home:
            old_home = MenuItem.objects.filter(site_home=True)
            for item in old_home:
                item.site_home = False
                item.save()
        super(MenuItem, self).save()

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('menu item')
        verbose_name_plural = _('menu items')

mptt.register(MenuItem)


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

    class Meta:
        verbose_name = _('layout')
        verbose_name_plural = _('layouts')


class BaseContent(models.Model):
    """Parent class for every content model.
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


class Source(models.Model):
    name = models.CharField(_('name'),max_length=250,
                             db_index=True, blank=False, unique=True)
    slug = AutoSlugField(populate_from='name', unique=True, db_index=True,
                         always_update=True)
    link = models.CharField(_('link'), max_length=250, blank=True, default='')

    def __unicode__(self):
        return self.name


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


#class Attachment(models.Model):
#    """A simple attachment model.
#    """
#    attachment =  models.FileField(_('image'), max_length=100, format='Image',
#                                    directory='pictures/')
#    name = models.CharField(_('name'),max_length=250,
#                             db_index=True, blank=False, unique=True)

#    class Meta:
#        verbose_name = _('attachment')
#        verbose_name_plural = _('attachment')


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

from registration_backends import CaptchaBackend
from registration import signals

def _create_profile_upon_activation(*args, **kwargs):
    UserProfile.objects.create(user=kwargs['user'])

signals.user_activated.connect(_create_profile_upon_activation)
