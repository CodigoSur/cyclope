#!/usr/bin/env python
# -*- coding: UTF-8 -*-
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
What is Cyclope
===============

:synopsys: Cyclope 3 is a django based CMS for pythonistas who don't mind coding a bit and dislike overly-complex user interfaces. It is based on the concept of categorized collections of heterogeneous content types with associated front-end views that can be laid out in the website's page regions. The goal of this project is to create a CMS that is friendly to the end user and versatile for the developer. It won't solve every complex problem at UI level but will let you "expose" the solution.
:copyright: 2010 by `Código Sur <http://www.codigosur.org>`_ -  Nuestra América Asoc. Civil / Fundación Pacificar
:url: http://codigo.cyclope.ws/
:version: 0.1.0
:licence: GPL v3

Target audience
---------------

``Cyclope`` is developed with three different audiences in mind:

1. Developers:

    We created ``Cyclope`` thinking of those developers that actually like to code in their language of choice: Python. They don't really look for a product that will let them accomplish even the most complex stuff from a web-based UI.

    We just aim at providing developers with the tools necessary to easily expose their content types and views for site managers to work with in the admin interface.

    Custom created content types and views can easily be packed in modules for drop-in re-utilization.

2. Site managers:

    They will use the Django admin interface to set up the website global settings, theme, layouts, menus, and categories.

3. Content editors:

    Will have access to a customized Django admin interface to create categories and content for the different content types and collections available in the website.


Documentation
-------------
...

Installation
------------

Please visit: codigo.cyclope.ws for installation instructions.


Demo project
------------

You can test ``Cyclope`` by running: :command:`python manage.py runserver` in the provided cyclope_demo/ folder.

The admin interface will be accessible at http://localhost:8000/admin and the fronted at: http://localhost:8000

Default username is: admin and the password: password.


Contact and Support
-------------------

If you need to contact the development team you can reach us by e-mail: nicoechaniz@codigosur.org


"""

VERSION = (0, 2, 0, 'beta')
__version__ = '.'.join(map(str, VERSION))
