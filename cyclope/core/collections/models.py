# *-- coding:utf-8 --*
"""
core.collections.models
-----------------------
Django models for generic categorization of content objects
"""

from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
import mptt
from autoslug.fields import AutoSlugField
import cyclope

class Collection(models.Model):
    """A facility for creating custom content collections."""

    name = models.CharField(_('name'), max_length=50, unique=True)
    slug = AutoSlugField(populate_from='name', always_update=True)
    is_navigation_root = models.BooleanField(_('is navigation root'),
                                             default=False)
    content_types = models.ManyToManyField(ContentType, db_index=True,
                                           verbose_name=_('content types'))
    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('collection')
        verbose_name_plural = _('collections')


class Category(models.Model):
    """Categories are associated with a specific Collection,
    and can be generically usable with any content type.
    """

    collection = models.ForeignKey(Collection,
        verbose_name=_('collection'), related_name=_('collection categories'))
    name = models.CharField(_('name'), max_length=50)
    slug = AutoSlugField(populate_from='name', always_update=True,
                         unique_with=('parent', 'collection'))
    parent = models.ForeignKey('self', verbose_name=_('parent'),
                              related_name=_('children'), null=True, blank=True)
    active = models.BooleanField(_('active'), default=True, db_index=True)
    description = models.TextField(_('description'), blank=True, null=True)

    def __unicode__(self):
        return self.name

    # this is needed for the feincms.editor.TreeEditor to correctly display the hierarchy
#    def get_absolute_url(self):
#        return self.__unicode__()

    def valid_parents(self):
        return Category.tree.filter(pk__isnot=self.pk)

    def get_instance_url(self, view_name=None):
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

    @classmethod
    def get_model_url(cls, view_name):
        return '%s/%s/View/%s'\
                % (cls._meta.app_label, cls._meta.object_name.lower(), view_name)

    class Meta:
        unique_together = ('collection', 'name')
        verbose_name = _('category')
        verbose_name_plural = _('categories')

mptt.register(Category)


class CategoryMapManager(models.Manager):

    def get_for_object(self, obj):
        """Get all Category Maps for an instance of a content object.

        Args:
          obj: a model or instance
        """

        ctype = ContentType.objects.get_for_model(obj)
        return self.filter(content_type__pk=ctype.pk, object_id=obj.pk)

    def get_for_ctype(self, ctype):
        """Get all Collection Categories available for this content_type.

        Args:
          ctype: a ContentType instance
        """
        return self.filter(content_type__pk=ctype.pk)


class CategoryMap(models.Model):
    """Mappings between a content object and it's associated categories."""

    category = models.ForeignKey('Category', verbose_name=_('category'),
                                 db_index=True, related_name='category_maps')
    content_type = models.ForeignKey(ContentType, db_index=True,
                                     verbose_name=_('content type'))
    object_id = models.PositiveIntegerField(db_index=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    objects = CategoryMapManager()

    def __unicode__(self):
        return '%(collection_name)s: %(category_name)s' % {
            'collection_name': self.category.collection.name,
            'category_name': self.category.name}

    class Meta:
        verbose_name = _('category map')
        verbose_name_plural = _('category maps')


class Collectible(models.Model):
    """
    Base class for collectible objects
    """
    categories = generic.GenericRelation(CategoryMap,
        content_type_field='content_type', object_id_field='object_id',
        verbose_name = _('categories'))

    # activate custom admin filter
    categories.category_filter = True

    @property
    def is_orphan(self):
        return not self.categories.exists()

    class Meta:
        abstract = True
