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

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.template import loader


from cyclope import views
from cyclope import settings as cyc_settings
from cyclope.core import frontend
from cyclope.utils import NamePaginator

from models import Contact


class ContactDetail(frontend.FrontendView):
    """Detail view for Contacts"""
    name='detail'
    verbose_name=_('detailed view of the selected Contact')
    is_default = True
    is_instance_view = True
    is_content_view = True

    def get_response(self, request, req_context, options, content_object):
        return views.object_detail(request, req_context, content_object)

frontend.site.register_view(Contact, ContactDetail)

class TeaserListOptions(forms.Form):
    items_per_page = forms.IntegerField(label=_('Items per page'), initial=3, min_value=1)
    order_by = forms.ChoiceField(label=_('Order by'),
                                 choices=(('given_name', _('given name')),
                                          ('surname', _('surname'))),
                                 initial='given_name')

class ContactTeaserList(frontend.FrontendView):
    """Teaser list view for Contacts.
    """
    name='teaser_list'
    verbose_name=_('list of Contact teasers')
    is_instance_view = False
    is_content_view = True
    is_region_view = True

    options_form = TeaserListOptions
    template = "contacts/contact_teaser_list.html"

    def get_response(self, request, req_context, options):
        contacts = Contact.objects.all()
        # Surname is optional, but Paginator needs the value if ordering for surname
        # so we cheat adding a temporary surname.
        for contact in contacts:
            if not contact.surname:
                contact.surname = "Aa fake name"
        paginator = NamePaginator(contacts, on=options["order_by"],
                                  per_page=options["items_per_page"])

        for contact in contacts:
            if contact.surname == "Aa fake name":
                contact.surname = ""

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
                            'page': page,
                            'view_options': options})
        t = loader.get_template(self.template)
        return t.render(req_context)

frontend.site.register_view(Contact, ContactTeaserList)
