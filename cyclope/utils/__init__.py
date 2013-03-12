#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010-2012 Código Sur Sociedad Civil
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
utils
-----

Helper methods and classes.
"""

import os
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import InvalidPage, EmptyPage
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
import cyclope

def get_extension(filename):
    """
    Returns lowercase extension of filename. Eg: get_extension(foo.Bar) -> "bar"
    """
    return os.path.splitext(filename)[1].lower().replace(".", "")

def menu_item_for_request(request):
    # Avoids a circular import
    from cyclope.models import MenuItem
    if getattr(request, "_menu_item", False) is not False:
        return request._menu_item
    req_url = request.path
    url = req_url[len(cyclope.settings.CYCLOPE_PREFIX)+1:]
    if url == '':
        try:
            # when no home menuitem has yet been set this will fail
            menu_item = MenuItem.objects.select_related().get(site_home=True)
        except:
            menu_item = None
    else:
        try:
            # match menuitems with internal and external (custom) urls
            menu_item = MenuItem.objects.select_related().get(Q(url=url)|Q(url=req_url))
        except:
            menu_item = None
    request._menu_item = menu_item
    return menu_item

def layout_for_request(request):
    """
    Returns the layout corresponding to the MenuItem matching the request URL
    or the default site layout if no matching MenuItem is found.
    """
    menu_item = menu_item_for_request(request)
    if menu_item:
        layout = menu_item.get_layout()
    else:
        if request.session.has_key('layout'):
            layout = request.session['layout']
        else:
            layout = cyclope.settings.CYCLOPE_DEFAULT_LAYOUT

    return layout


def template_for_request(request):
    """
    Returns the template corresponding to the MenuItem.layout
    matching the request or the default site template
    if no matching MenuItem is found.
    """
    layout = layout_for_request(request)
    template = 'cyclope/themes/%s/%s' % (
                cyclope.settings.CYCLOPE_CURRENT_THEME,
                layout.template
                )
    return template


from django.utils.functional import Promise
from django.utils.translation import force_unicode
from django.utils.simplejson import JSONEncoder

# snippet from http://code.djangoproject.com/ticket/5868
# to fix json encoding of lazy translated strings
class LazyJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, Promise):
            return force_unicode(o)
        else:
            return super(LazyJSONEncoder, self).default(o)

# copied from django.templates.defaultfilters
def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    import unicodedata, re
    value = unicode(value)
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
    return re.sub('[-\s]+', '-', value)

import string
from django.core.paginator import InvalidPage, EmptyPage
import unicodedata

def remove_accents(string):
    nkfd_form = unicodedata.normalize('NFKD', unicode(string))
    only_ascii = nkfd_form.encode('ASCII', 'ignore')
    return only_ascii

class NamePaginator(object):
    """Pagination for string-based objects"""
    # Based on http://djangosnippets.org/snippets/1364/

    def __init__(self, object_list, on=None, per_page=25):
        self.object_list = object_list
        self.count = len(object_list)
        self.pages = []

        # chunk up the objects so we don't need to iterate over the whole list for each letter
        chunks = {}

        for obj in self.object_list:
            if on:
                if "." in on:
                    obj_str = unicode(reduce(getattr, on.split("."), obj))
                else:
                    obj_str = unicode(getattr(obj, on))
            else: obj_str = unicode(obj)

            letter = remove_accents(obj_str[0]).upper()

            if letter not in chunks: chunks[letter] = []

            chunks[letter].append(obj)

        # the process for assigning objects to each page
        current_page = NamePage(self)

        for letter in string.ascii_uppercase:
            if letter not in chunks:
                current_page.add([], letter)
                continue

            sub_list = chunks[letter] # the items in object_list starting with this letter

            new_page_count = len(sub_list) + current_page.count
            # first, check to see if sub_list will fit or it needs to go onto a new page.
            # if assigning this list will cause the page to overflow...
            # and an underflow is closer to per_page than an overflow...
            # and the page isn't empty (which means len(sub_list) > per_page)...
            if new_page_count > per_page and \
                    abs(per_page - current_page.count) < abs(per_page - new_page_count) and \
                    current_page.count > 0:
                # make a new page
                self.pages.append(current_page)
                current_page = NamePage(self)

            current_page.add(sub_list, letter)

        # if we finished the for loop with a page that isn't empty, add it
        if current_page.count > 0: self.pages.append(current_page)

    def page(self, num):
        """Returns a Page object for the given 1-based page number."""
        if len(self.pages) == 0:
            return NamePage(self)
        elif num > 0 and num <= len(self.pages):
            return self.pages[num-1]
        else:
            raise InvalidPage

    @property
    def num_pages(self):
        """Returns the total number of pages"""
        return len(self.pages)

class NamePage(object):
    def __init__(self, paginator):
        self.paginator = paginator
        self.object_list = []
        self.letters = []

    @property
    def count(self):
        return len(self.object_list)

    @property
    def start_letter(self):
        if len(self.letters) > 0:
            self.letters.sort(key=str.upper)
            return self.letters[0]
        else: return None

    @property
    def end_letter(self):
        if len(self.letters) > 0:
            self.letters.sort(key=str.upper)
            return self.letters[-1]
        else: return None

    @property
    def number(self):
        return self.paginator.pages.index(self) + 1

    def add(self, new_list, letter=None):
        if len(new_list) > 0: self.object_list = self.object_list + new_list
        if letter: self.letters.append(letter)

    def __repr__(self):
        if not self.start_letter:
            return "<Page: empty>"
        if self.start_letter == self.end_letter:
            return u"%c" % (self.start_letter, )
        else:
            return u'%c-%c' % (self.start_letter, self.end_letter)

def get_page(paginator, request):
    """
    Returns the current paginator instance page. Page number of paginator
    is determined by request.GET["page"].
    """
    # Make sure page request is an int. If not, deliver first page.
    try:
        page_number = int(request.GET.get('page', '1'))
    except ValueError:
        page_number = 1

    # DjangoDocs uses page differently
    # If page request (9999) is out of range, deliver last page of results.
    try:
        page = paginator.page(page_number)
    except (EmptyPage, InvalidPage):
        page = paginator.page(paginator.num_pages)

    return page




def _invalidate_cache(sender, **kwargs):
    sender._instance = None

def get_singleton(model_class):
    """
    Returns the instance with id=1 of the Model Class
    """
    from django.db.models.signals import post_save
    try:
        if not hasattr(model_class, "_instance"):
            post_save.connect(_invalidate_cache, sender=model_class)
        if not getattr(model_class, "_instance", None):
            model_class._instance = model_class.objects.get(id=1)
        return model_class._instance
    except model_class.DoesNotExist, e:
        e.args = (e.args[0] +" At least one instance of this class must exists.", )
        raise e

def get_or_set_cache(func, args, kwargs, key, timeout=None):
    from django.core.cache import cache
    out = cache.get(key)
    if out is None:
        out = func(*args, **kwargs)
        cache.set(key, out, timeout)
    return out

class PermanentFilterMixin(object):
    """
    Mixin class that adds a default filter to a changelist that also is permanent
    (saved in the session).

    You must define permanent_filters in the subclass, something like this:

    permanent_filters = (
        (u"model__id__exact", # this is the key of the filter
         lambda request: unicode(Model.objects.all()[0].id)), # default param as lambda
    )

    And then use the method do_permanent_filters in the change_list
    """
    permanent_filters = None

    def do_permanent_filters(self, request):
        for filter_key, default_filter_param in self.permanent_filters:
            session_key = "%s|%s" % (request.path, filter_key)
            if not request.GET.get(filter_key):
                param = request.session.get(session_key) or default_filter_param(request)
                if param:
                    GET = request.GET.copy()
                    GET[filter_key] = param
                    request.GET = GET
            request.session[session_key] = request.GET.get(filter_key)


class ThumbnailMixin(object):

    def get_thumbnail_src(self):
        try:
            image = getattr(self, "image")
        except AttributeError:
            raise NotImplemented
        return getattr(image, "url_thumbnail")

    def thumbnail(self):
        return '<img class="thumbnail" src="%s"/>' %  self.get_thumbnail_src()

    thumbnail.short_description = _('Thumbnail Image')
    thumbnail.allow_tags = True


class CrispyFormsSimpleMixin(object):
    helper = FormHelper()
    helper.add_input(Submit('submit', _('Submit')))


from django.conf import settings
from django.core.mail.message import EmailMultiAlternatives
from django.contrib.auth.models import Group

def _get_managers_mails():
    emails = [a[1] for a in settings.MANAGERS]
    try:
        emails.extend(Group.objects.get(name="managers").user_set.values_list("email",
                                                                             flat=True))
    except Group.DoesNotExist:
        pass

    return filter(None, emails)

def mail_managers(subject, message, fail_silently=False, connection=None,
                  html_message=None):
    """
    Sends a message to the managers, as defined by the MANAGERS setting and
    to the users in managers group."""

    emails = _get_managers_mails()
    if not emails:
        return
    mail = EmailMultiAlternatives(u'%s%s' % (settings.EMAIL_SUBJECT_PREFIX, subject),
                message, settings.SERVER_EMAIL, emails, connection=connection)
    if html_message:
        mail.attach_alternative(html_message, 'text/html')
    mail.send(fail_silently=fail_silently)
