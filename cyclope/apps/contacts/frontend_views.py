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


from django.utils.translation import ugettext_lazy as _

from cyclope.core import frontend
from cyclope import views
from cyclope import settings as cyc_settings

from models import Contact


class ContactDetail(frontend.FrontendView):
    """Detail view for Contacts"""
    name='detail'
    verbose_name=_('detailed view of the selected Contact')
    is_default = True
    is_instance_view = True
    is_content_view = True

    def get_response(self, request, req_context, content_object):
        context = {'content_relations': content_object.related_contents.all()}
        return views.object_detail(request, req_context, content_object,
                                   extra_context=context)

frontend.site.register_view(Contact, ContactDetail)


class ContactTeaserList(frontend.FrontendView):
    """Teaser list view for Contacts.
    """
    name='teaser_list'
    verbose_name=_('list of Contact teasers')
    is_instance_view = False
    is_content_view = True
    is_region_view = True

    def get_response(self, request, req_context):
        return views.object_list(request, req_context,
                                 Contact.objects.all(), view_name=self.name)


frontend.site.register_view(Contact, ContactTeaserList)

class ContactAlphabeticalTeaserList(frontend.FrontendView):
    """ An alphabeticaly sorted list view of contacts.
    """
    name='alphabetical_teaser_list'
    verbose_name=_('alphabetical teaser list of Contact members')
    items_per_page = cyc_settings.CYCLOPE_PAGINATION['TEASER']
    is_content_view = True
    is_region_view = True

    template = "contacts/alphabetical_teaser_list.html"

    def get_response(self, request, req_context, content_object):
        paginator = NamePaginator(Contact.objects.all(), on="name", per_page=self.items_per_page)

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

        req_context.update({'contacts': page.object_list,
                            'page': page})
        t = loader.get_template(self.template)
        return t.render(req_context)

frontend.site.register_view(Contact, ContactAlphabeticalTeaserList)
