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

class LayoutMiddleware(object):
    """
    Sets session['layout'] if the current menu item has a persistent layout
    and clears it when another menu_item changes the layout.
    """
    def process_request(self, request):
        import cyclope # Leave this here, it prevents circular imports
        import cyclope.settings # Leave this here

        menu_item = cyclope.utils.menu_item_for_request(request)
        if menu_item:
            ## we force the layout for items with custom URL (external apps)
            ## so they can use the correct template to extend from
            if menu_item.persistent_layout or menu_item.custom_url:
                layout = menu_item.get_layout()
                request.session['layout'] = layout
                request.session['layout_template'] = layout.get_template_path()

            else:
                if request.session.has_key('layout'):
                    del request.session['layout']
        else:
            ## if no layout_template has been set we set it to the default so external apps'
            ## templates that extend from request.session.layout_template won't break
            ## even when accessed through a direct URL
            if not 'layout_template' in request.session and \
                   hasattr(cyclope.settings, 'CYCLOPE_DEFAULT_TEMPLATE'):
                request.session['layout_template'] = cyclope.settings.CYCLOPE_DEFAULT_TEMPLATE


